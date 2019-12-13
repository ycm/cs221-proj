# Comparative reconstruction of Middle Chinese with deep learning

🌲 Andrew Yang, Ken Hong, Nash Luxsuwong | CS 221 🌲

This project aims to apply machine learning to comparative linguistic reconstruction. Many East Asian languages today have standardized pronunciations for Chinese characters. The character for `middle' is pronounced /ʈʂɔŋ/ in Mandarin, /t͡sʊŋ/ in Cantonese, /tɕuŋ/ in Korean, etc. Using the known pronunciation of Chinese characters in modern Sinitic and Sino-Xenic languages, historical linguists have created reconstructions ancestors of modern Chinese languages thought to exist a long time ago.

We focus on reconstructions of Middle Chinese, an archaic prestige variety of Chinese spoken over a thousand years ago. We parsed Wiktionary to gather the pronunciations of over 15,000 Chinese characters in East Asian languages as diverse as Mandarin, Japanese, and Korean, and aligned them to reconstructed pronunciations devised by influential historical linguists such as Bernhard Karlgren \cite{Karlgren} and others (also from Wiktionary). Because individual reconstruction schemes are not directly comparable, we are working only with Karlgren's system at the moment. 

For an in-depth explanation of our goals and results, please consult the files in `/deliverables/`.

The following is a brief overview of the codebase:

#### / (root)

This folder mainly contains the implementations of the models themselves.

The baseline model is in `baseline-model.ipynb`. The LR-1 model is in `model-logreg.ipynb`. The LR-2 model is in `model-one-vs-rest-lr.ipynb`. The MLP-1 model is in `model-nn-keras.ipynb`. The grid search and cross validation for MLP-2 are in `model-nn-2-keras-cv-and-grid-search.ipynb`. The final implementation and parameters for MLP-2 are in `model-nn-2-keras-final.ipynb`. 

#### /preprocessing/dataset/

The relevant files are `script.py`, `script2.py`, `scriptcomp.py`, which were respectively used to scrape pronunciation data for Japanese, Korean, Mandarin, Cantonese, Middle Chinese, as well as character composition data from a Wiktionary full dump. The `lxml` package was used with `iterparse` to parse the ~7GB file.

The scraped data is cleaned up with `first_processing`, `second_processing`, and `third_processing`, in that order. By the end, the dataset is available as `processed2.pkl`, which is passed to the model notebooks.

The `csv` files and `xlsx` files, along with the `output` folders are intermediary products of scraping and processing.

#### /model/

This folder contains the data matrices that we our models load and train on.

#### /figs/

This folder contains relevant figures and graphs that we included in our poster and final report.

#### /deliverables/

This folder contains the project proposal, progress report, poster, and final report, as well as a sample of our data.
