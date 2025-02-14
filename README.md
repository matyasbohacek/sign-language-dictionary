COVER IMAGE TBD

# Towards an AI-Driven Video-Based American Sign Language Dictionary: Exploring Design and Usage Experience with Learners

#### [Saad Hassan](https://saadh.info), [Matyas Bohacek](https://www.matyasbohacek.com), [Chaelin Kim](https://chaelin0722.github.io/), and [Denise Crochet](https://liberalarts.tulane.edu/linguistics/people/faculty/denise-crochet)

Searching for unfamiliar American Sign Language (ASL) signs is challenging for learners because, unlike spoken languages, they cannot type a text-based query to look up an unfamiliar sign. Advances in isolated sign recognition have enabled the creation of video-based dictionaries, allowing users to submit a video and receive a list of the closest matching signs. Previous HCI research using Wizard-of-Oz (WoZ) prototypes has explored interface designs for ASL dictionaries. Building on these studies, we incorporate their design recommendations and leverage state-of-the-art sign-recognition technology to develop an automated video-based dictionary. We also present findings from an observational study with twelve novice ASL learners who used this dictionary during video-comprehension and question-answering tasks. Our results address human-AI interaction challenges not covered in previous WoZ research, including recording and resubmitting signs, unpredictable outputs, system latency, and privacy concerns. These insights offer guidance for designing and deploying video-based ASL dictionary systems.

> [See paper]() — [Contact us](mailto:maty-at-stanford-dot-edu)
> 
> _Pre-print released on arXiv_

## Getting Started

1. Clone this repo:

```shell
git clone https://github.com/matyasbohacek/sign-language-dictionary.git
```

2. In the `sign-language-dictionary` directory, set up a Python environment (Python 3.9 is recommended):

```shell
conda create -n sign-language-dictionary python=3.9
```

3. Install required Python dependencies using:

```shell
conda activate sign-language-dictionary
pip install -r requirements.txt
```

4. Set up hosting for the [`detailed-analysis`](detailed-analysis/) web interface. You can host this on localhost or remote (FTP hosting was tested to work).

5. Then, proceed to `main-dictionary-interface/app.py` and update `DETAILED_ANALYSIS_URL` and `GIFS_DIR_URL`. Optionally, update `LOGO_PATH_URL` and `CONTACT_EMAIL` in `main-dictionary-interface/constants.py`. Then, proceed to `detailed-analysis/index.html` and update `DETAILED_ANALYSIS_URL`, `GLOSS_SPECIFIER_URL`, `GIFS_DIR_URL`, and `HANDSHAPE_IMG_DIR_URL`.

6. Start the dictionary (web interface):

```shell
python -m app
```

## Features

**Feature.** Description

## Citation

```bibtex
TBD
```

## Remarks & Updates

- (**TBD Date**) The pre-print is released on arXiv.
