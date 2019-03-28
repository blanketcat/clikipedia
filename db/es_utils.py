import elasticsearch


def get_client():
	es = elasticsearch.Elasticsearch()
	return es


def write_article_to_index(index=str, doctype=str, id=int, body={}):
	es = get_client()
	es.index(
		index=index,
		doctype=doctype,
		id=id,
		body=body
	)

