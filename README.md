# Crowdsourcing Task for Collecting Hashtag-Context Mapping

Hashtags of social media posts contain information on the context of the posts. However, hashtags often consist of only a couple of words, and the set of tags could give a new meaning apart from the meaning of each hashtag. Furthermore, some hashtags contain multiple words without proper punctuation. Such problems make it hard to classify hashtags into appropriate context categories. 

To overcome such issue, this crowdsourcing task enables its users to crowdsource hashtags and their classifications. The task supports two types of tasks: a) asking workers to share hashtags from their own Instagram posts and classify the tags or b) asking workers to share hashtags by making hypothetical Instagram posts and classify the tags.  

To support workers to efficiently conduct the task, the task contains an integrated NLP pipeline to suggest an appropriate context classification for each hashtag. The pipeline can be enabled by switching to ```hybrid``` branch.

## Installation

```bash
git clone https://github.com/kixlab/suggestbot-instagram-context-annotator
pip install -r requirements.txt
```

## Running

```bash
python manage.py runserver
```

The explanation of the task could be accessed from ```/start``` page.
