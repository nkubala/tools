#!/usr/bin/python

import json
import logging
from subprocess import check_output, Popen, PIPE, CalledProcessError

logging.getLogger().setLevel(logging.INFO)

def main():
	versions = retrieve_all_versions()
	for version in versions:
		logging.info('deleting version %s' % version)
		delete_version(version)
	return 0


def retrieve_all_versions():
	command = ['gcloud', 'app', 'versions', 'list',
			   '--service', 'default', '--format', 'json']
	proc = Popen(command, shell=False, stdout=PIPE, stderr=PIPE, stdin=PIPE)
	output, err = proc.communicate()

	versions = json.loads(output)
	return [version['id'] for version in versions]


def delete_version(version):
	command = ['gcloud', 'app', 'versions', 'delete',
			   '--service', 'default', version, '-q']
	try:
		check_output(command)
	except CalledProcessError as cpe:
		logging.error('Error encountered when deleting app version! %s',
					  cpe.output)
	return 0


if __name__ == '__main__':
	main()
