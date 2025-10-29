from Shaurmania.settings import DEBUG, COMPRESS_ENABLED, IS_HALLOWEEN, IS_NEW_YEAR

def feature_flags(request):
	return {
		'DEBUG'            : DEBUG,
		'COMPRESS_ENABLED' : COMPRESS_ENABLED,
		'IS_HALLOWEEN'     : IS_HALLOWEEN,
		'IS_NEW_YEAR'      : IS_NEW_YEAR
	}
