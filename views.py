# -*- encoding: utf-8 ---------------------------------------------------------


from serve import *
from models import *


class Table():
    def __init__(self, heading, column_names, rows):
        self.heading = heading
        self.column_names = column_names
        self.rows = rows


def url_for(Model, dataset_id, topicmodel_id, id):
    return '/dataset/{}/topic_model/{}/{}/{}'.format(dataset_id, topicmodel_id,
        Model.__tablename__, id)


@app.route('/')
@app.route('/index.html')
def index():
    datasets = Dataset.query.all()
    return render_template('index.html', datasets=datasets)


@app.route('/dataset/<int:dataset_id>/topic_model/<int:topicmodel_id>')
def topic_model(dataset_id, topicmodel_id):
    return render_template('topic_model.html',
        dataset=Dataset.query.get(dataset_id),
        topicmodel=TopicModel.query.get((dataset_id, topicmodel_id)),
        top_ten_topics=Topic.query.filter_by(
            topicmodel=topicmodel_id).order_by('probability')[-10:])


@app.route('/dataset/<int:dataset_id>/topic_model/<int:topicmodel_id>'
           '/browse_topics.html')
def browse_topics(dataset_id, topicmodel_id):
    return render_template('browse_topics.html',
        dataset=Dataset.query.get(dataset_id),
        topicmodel=TopicModel.query.get((dataset_id, topicmodel_id)),
        topics=Topic.query.filter_by(
            topicmodel=topicmodel_id).
            order_by('probability')[::-1])


@app.route('/dataset/<int:dataset_id>/topic_model/<int:topicmodel_id>'
           '/topic/<int:topic_id>')
def topic(dataset_id, topicmodel_id, topic_id):
    topic_terms = TopicTerm.query.filter_by(topicmodel=topicmodel_id,
        topic=topic_id)
    terms = Term.query.filter(id in [tt.term for tt in topic_terms.all()])
    document_topics = DocumentTopic.query.filter_by(topicmodel=topicmodel_id,
        topic=topic_id)
    documents = Document.query.filter(
        id in [dt.document for dt in document_topics.all()])

    terms_wt_table = Table(
        heading='Terms sorted by p(w|t)',
        column_names=['p(w|t)', 'Term'],
        rows=[[tt.prob_wt, url_for(Term, dataset_id, topicmodel_id, tt.term),
            Term.query.get((tt.term, dataset_id)).text]
            for tt in topic_terms.order_by('prob_wt')[::-1]]
    )

    terms_tw_table = Table(
        heading='Terms sorted by p(t|w)',
        column_names=['p(t|w)', 'Term'],
        rows=[[tt.prob_tw, url_for(Term, dataset_id, topicmodel_id, tt.term),
            Term.query.get((tt.term, dataset_id)).text]
            for tt in topic_terms.order_by('prob_tw')[::-1]]
    )

    return render_template('topic.html',
        dataset=Dataset.query.get(dataset_id),
        topicmodel=TopicModel.query.get((dataset_id, topicmodel_id)),
        topic=Topic.query.get((topicmodel_id, topic_id)),
        terms_wt_table=terms_wt_table,
        terms_tw_table=terms_tw_table,
        documents_dt_table=documents_dt_table,
        documents_td_tbale=documents_td_table)


@app.route('/dataset/<int:dataset_id>/topic_model/<int:topicmodel_id>/'
           'term/<int:term_id>')
def term(dataset_id, topicmodel_id, term_id):
    return render_template('term.html',
        dataset=Dataset.query.get(dataset_id),
        topicmodel=TopicModel.query.get((dataset_id, topicmodel_id)))


@app.route('/dataset/<int:dataset_id>/topic_model/<int:topicmodel_id>/'
           'document/<int:document_id>')
def document(dataset_id, topicmodel_id, document_id):
    return render_template('document.html',
        dataset=Dataset.query.get(dataset_id),
        topicmodel=TopicModel.query.get((dataset_id, topicmodel_id)))
