def safe_load_settings(field, settings):
	if field in settings:
		return True, settings[field], "Load {} : {}".format(field, settings[field])
	return False, None, "Unable to load {}".format(field)

