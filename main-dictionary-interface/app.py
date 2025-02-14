
import copy
import statistics
import torch
import cv2

import numpy as np
import gradio as gr
import pandas as pd

from constants import FORCE_LIGHT_MODE_JS_SCRIPT, HEAD_HTML, DESCRIPTION_HTML, GLOSS, POTENTIAL_WARNING_MESSAGE, NO_RESPONSE_MESSAGE, COMPACT_RESULTS_HTML
from spoter_mod.skeleton_extractor import obtain_pose_data
from spoter_mod.normalization.body_normalization import normalize_single_dict as normalize_single_body_dict, BODY_IDENTIFIERS
from spoter_mod.normalization.hand_normalization import normalize_single_dict as normalize_single_hand_dict, HAND_IDENTIFIERS


# TODO: Update this to be the hosted detailed analysis web app, with the origin parameter set to the hosted path of
#  your main dictionary interface
DETAILED_ANALYSIS_URL = ""
# e.g., https://www.mydetailedanalysishosting.com/index.html?origin=https://www.mymaindictionaryinterfacehosting.com

# TODO: Update this to be the path to the hosted directory of gifs
GIFS_DIR_URL = ""
# e.g., https://www.mydetailedanalysishosting.com/gifs/


df = pd.read_csv("gloss-specifier.csv", encoding="utf-8")
df = df.fillna("—")

model = torch.load("spoter-checkpoint.pth", map_location=torch.device('cpu'))
model.train(False)

HAND_IDENTIFIERS = [id + "_Left" for id in HAND_IDENTIFIERS] + [id + "_Right" for id in HAND_IDENTIFIERS]


device = torch.device("cpu")
if torch.cuda.is_available():
    device = torch.device("cuda")


def tensor_to_dictionary(landmarks_tensor: torch.Tensor) -> dict:

    data_array = landmarks_tensor.numpy()
    output = {}

    for landmark_index, identifier in enumerate(BODY_IDENTIFIERS + HAND_IDENTIFIERS):
        output[identifier] = data_array[:, landmark_index]

    return output


def dictionary_to_tensor(landmarks_dict: dict) -> torch.Tensor:

    output = np.empty(shape=(len(landmarks_dict["leftEar"]), len(BODY_IDENTIFIERS + HAND_IDENTIFIERS), 2))

    for landmark_index, identifier in enumerate(BODY_IDENTIFIERS + HAND_IDENTIFIERS):
        output[:, landmark_index, 0] = [frame[0] for frame in landmarks_dict[identifier]]
        output[:, landmark_index, 1] = [frame[1] for frame in landmarks_dict[identifier]]

    return torch.from_numpy(output)


def greet(video, progress=gr.Progress()):

    if not video:
        return NO_RESPONSE_MESSAGE

    video_cap = cv2.VideoCapture(video)

    width = video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = video_cap.get(cv2.CAP_PROP_FPS)

    trigger_warning = False

    if width < 600 or height < 400:
        trigger_warning = True

    if fps < 20:
        trigger_warning = True

    ###

    # Initialize variables
    frames_analyzed = -1
    faces_centered = []
    num_faces_detected = []

    # Load the pre-trained Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Step 3: Face detection and center check
    while True:
        ret, frame = video_cap.read()
        frames_analyzed += 1
        if not ret:
            break  # Break the loop if there are no frames left to read

        # For efficiency, you may want to analyze fewer frames
        # Example: Analyze every 30th frame
        if frames_analyzed % 30 != 0:
            continue

        # Convert to grayscale for the Haar cascade detector
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Check if exactly one face is detected and its position
        num_faces_detected.append(len(faces))
        if len(faces) == 1:
            x, y, w, h = faces[0]
            # Calculate the center of the face
            face_center = (x + w // 2, y + h // 2)
            video_center = (width // 2, height // 2)

            # Step 4: Check if the face is in the center
            if abs(face_center[0] - video_center[0]) < width * 0.5 and abs(face_center[1] - video_center[1]) < height * 0.5:
                faces_centered.append(1)
            else:
                faces_centered.append(0)

    video_cap.release()  # Release the video file

    if faces_centered:
        if statistics.mean(faces_centered) < 0.5:
            trigger_warning = True

    if len([1 for x in num_faces_detected if x == 0]) > len(num_faces_detected) / 2 or len([1 for x in num_faces_detected if x >= 2]) > len(num_faces_detected) / 2:
        trigger_warning = True

    ###

    data = obtain_pose_data(video, progress=progress)

    depth_map = np.empty(shape=(len(data.data_hub["nose_X"]), len(BODY_IDENTIFIERS + HAND_IDENTIFIERS), 2))

    for index, identifier in enumerate(BODY_IDENTIFIERS + HAND_IDENTIFIERS):
        depth_map[:, index, 0] = data.data_hub[identifier + "_X"]
        depth_map[:, index, 1] = data.data_hub[identifier + "_Y"]

    depth_map = torch.from_numpy(np.copy(depth_map))

    depth_map = tensor_to_dictionary(depth_map)

    keys = copy.copy(list(depth_map.keys()))
    for key in keys:
        data = depth_map[key]
        del depth_map[key]
        depth_map[key.replace("_Left", "_0").replace("_Right", "_1")] = data

    depth_map = normalize_single_body_dict(depth_map)
    depth_map = normalize_single_hand_dict(depth_map)

    keys = copy.copy(list(depth_map.keys()))
    for key in keys:
        data = depth_map[key]
        del depth_map[key]
        depth_map[key.replace("_0", "_Left").replace("_1", "_Right")] = data

    depth_map = dictionary_to_tensor(depth_map)

    depth_map = depth_map - 0.5

    inputs = depth_map.squeeze(0).to(device)
    try:
        outputs = model(inputs).expand(1, -1, -1)
    except:
        return "<div style='padding: 5%;'>" + POTENTIAL_WARNING_MESSAGE + "</div>"

    results = torch.nn.functional.softmax(outputs, dim=2).detach().numpy()[0, 0]

    results = {GLOSS[i]: float(results[i]) for i in range(len(GLOSS))}

    NUM_TO_INCLUDE = 10
    class_indices = []
    class_confs = []

    for pred_class in sorted(results, key=results.get, reverse=True)[:NUM_TO_INCLUDE]:
        class_indices.append(pred_class.upper())
        # class_indices.append(df[df["Sign"] == pred_class.upper()].to_dict(orient='records')[0]["WLASL Identifier"])
        if int(results[pred_class] * 100):
            class_confs.append(int(results[pred_class] * 100))
        else:
            class_confs.append(1)

    full_analysis_url = DETAILED_ANALYSIS_URL + "?__theme=light&pred=" + ",".join(
        [str(i) for i in class_indices]) + "&conf=" + ",".join([str(i) for i in class_confs])

    top_pred_class = sorted(results, key=results.get, reverse=True)[0]
    top_pred_conf = class_confs[0]
    top_pred_item = df[df["Sign"] == str(class_indices[0])].to_dict(orient='records')[0]

    tag_0 = """<span style='opacity: 0.7;'>Movement:</span> """
    tag_1 = """, <span style='opacity: 0.7;'># Hands:</span> """
    tag_2 = """, <span style='opacity: 0.7;'>Location:</span> """
    tag_3 = """, <span style='opacity: 0.7;'>Handshape:</span> """
    top_pred_description = tag_0 + str(top_pred_item["Movement"]).capitalize() + tag_1 + str(top_pred_item[
                                                                                                 "Number of Hands"]).capitalize() + tag_2 + str(top_pred_item["Location"]).capitalize() + tag_3 + str(top_pred_item["Handshape"]).capitalize()
    top_pred_description = "no description"

    top_pred_description = str("Movement: " + top_pred_item["Movement"]).capitalize() + ", Num. of hands: " + str(int(top_pred_item["Number of Hands"])).capitalize() + ", Location: " + str(top_pred_item["Location"]).capitalize() + ", Handshape: " + str(top_pred_item["Handshape"]).capitalize()
    runner_up_alternatives = sorted(results, key=results.get, reverse=True)[1:7]

    gif_paths = [GIFS_DIR_URL + alt + ".gif" for alt in runner_up_alternatives]

    ###
    ind = 2

    runner_up_html_1 = []
    for gif_path, alt_name in zip(gif_paths[:2], runner_up_alternatives[:2]):
        annotations_data = df[df["Sign"] == str(alt_name.upper())].to_dict(orient='records')[0]
        annotations_desc = str("Movement: " + annotations_data["Movement"]).capitalize() + ", Num. of hands: " + str(int(annotations_data["Number of Hands"])).capitalize() + ", Location: " + str(annotations_data["Location"]).capitalize() + ", Handshape: " + str(annotations_data["Handshape"]).capitalize()

        alt_name = "#" + str(ind) + " " + alt_name.capitalize()

        runner_up_html_1.append(f"""
        <div class="runner-up" style="flex: 1; padding: 5px; box-sizing: border-box;">
            <div style="width: 100%; height: 0; padding-bottom: 56.25%; position: relative;">
                <img src="{gif_path}" alt="{alt_name}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;">
            </div>
            <span style="margin-top: 5px; text-align: left;"><p style="font-family: GraphikBold; text-alignment: left; font-size: 1.2em; padding-bottom: 0;">{alt_name}</p><p style="font-family: Graphik; text-alignment: left; margin-top: -5px;">{annotations_desc}</p></span>
        </div>
        """)

        ind += 1

    runner_up_html_1 = "\n".join(runner_up_html_1)

    runner_up_html_2 = []
    for gif_path, alt_name in zip(gif_paths[2:4], runner_up_alternatives[2:4]):
        annotations_data = df[df["Sign"] == str(alt_name.upper())].to_dict(orient='records')[0]
        annotations_desc = str("Movement: " + annotations_data["Movement"]).capitalize() + ", Num. of hands: " + str(int(annotations_data["Number of Hands"])).capitalize() + ", Location: " + str(annotations_data["Location"]).capitalize() + ", Handshape: " + str(annotations_data["Handshape"]).capitalize()

        alt_name = "#" + str(ind) + " " + alt_name.capitalize()
        runner_up_html_2.append(f"""
            <div class="runner-up" style="flex: 1; padding: 5px; box-sizing: border-box;">
                <div style="width: 100%; height: 0; padding-bottom: 56.25%; position: relative;">
                    <img src="{gif_path}" alt="{alt_name}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;">
                </div>
                <span style="margin-top: 5px; text-align: left;"><p style="font-family: GraphikBold; text-alignment: left; font-size: 1.2em; padding-bottom: 0;">{alt_name}</p><p style="font-family: Graphik; text-alignment: left; margin-top: -5px;">{annotations_desc}</p></span>
            </div>
            """)

        ind += 1

    runner_up_html_2 = "\n".join(runner_up_html_2)

    runner_up_html_3 = []
    for gif_path, alt_name in zip(gif_paths[4:], runner_up_alternatives[4:]):
        annotations_data = df[df["Sign"] == str(alt_name.upper())].to_dict(orient='records')[0]
        annotations_desc = str("Movement: " + annotations_data["Movement"]).capitalize() + ", Num. of hands: " + str(int(annotations_data["Number of Hands"])).capitalize() + ", Location: " + str(annotations_data["Location"]).capitalize() + ", Handshape: " + str(annotations_data["Handshape"]).capitalize()

        alt_name = "#" + str(ind) + " " + alt_name.capitalize()
        runner_up_html_3.append(f"""
                <div class="runner-up" style="flex: 1; padding: 5px; box-sizing: border-box;">
                    <div style="width: 100%; height: 0; padding-bottom: 56.25%; position: relative;">
                        <img src="{gif_path}" alt="{alt_name}" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover;">
                    </div>
                    <span style="margin-top: 5px; text-align: left;"><p style="font-family: GraphikBold; text-alignment: left; font-size: 1.2em; padding-bottom: 0;">{alt_name}</p><p style="font-family: Graphik; text-alignment: left; margin-top: -5px;">{annotations_desc}</p></span>
                </div>
                """)

        ind += 1

    runner_up_html_3 = "\n".join(runner_up_html_3)
    ###

    gif_path = GIFS_DIR_URL + str(class_indices[0]) + ".gif"

    score_confidence_interpretation = ""
    if top_pred_conf < 33:
        score_confidence_interpretation = "<span style='color: #F4442E; opacity: 0.7; font-weight: 500;'>Unlikely</span>"
    elif top_pred_conf < 66:
        score_confidence_interpretation = "<span style='color: #FDBB2F; opacity: 0.7; font-weight: 500;'>Possibly</span>"
    else:
        score_confidence_interpretation = "<span style='color: #3EC300; opacity: 0.7; font-weight: 500;'>Probably</span>"

    warning_message = ""
    if trigger_warning:
        warning_message = POTENTIAL_WARNING_MESSAGE

    return [COMPACT_RESULTS_HTML.replace("$WARNING_MESSAGE$", warning_message).replace("$URL$", full_analysis_url).replace("$ALTERNATIVES$", ", ".join(runner_up_alternatives)).replace("$TOP_PRED_CLASS$", "#1 " + top_pred_class.capitalize()).replace("$TOP_PRED_CONF$", str(score_confidence_interpretation)).replace("$GIF_PATH$", gif_path).replace("$DESCRIPTION$", top_pred_description).replace("$ALTERNATIVES_TABLE_1$", runner_up_html_1).replace("$ALTERNATIVES_TABLE_2$", runner_up_html_2).replace("$ALTERNATIVES_TABLE_3$", runner_up_html_3)]

label = [gr.HTML(label="Results")]
with open('styles.css') as f: css_c = f.read()

with gr.Blocks(title="ASL Dictionary", head=HEAD_HTML, css=css_c) as demo:
    x = gr.Interface(fn=greet, inputs=[gr.Video(sources=["webcam", "upload"], label="This video is not stored.")], outputs=label, js=FORCE_LIGHT_MODE_JS_SCRIPT,
                     head=HEAD_HTML,
                     title="ASL Dictionary", thumbnail="./static/favicon.png",
                     description=DESCRIPTION_HTML,
                     css="""styles.css""",
                     cache_examples=True,
                     allow_flagging="never"
                     )

demo.launch(
    debug=True,
    server_port=4080,
    server_name="0.0.0.0",
    allowed_paths=["fonts", "static"] # note: you might have to modify these to absolute paths
)
