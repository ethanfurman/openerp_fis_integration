.PHONY: srf srf3 whc whc3

srf:
	# copy schema and related files
	cp fis-oe.mixins/srf/FIS_SCHEMA fis-oe.source/
	# copy python2 pytz package
	rm -rf fis-oe.source/pytz
	rsync --archive fis-oe.mixins/pytz2 fis-oe.source/pytz
	# create new version
	/usr/local/bin/pyzapp create fis-oe.source -f --shebang "/usr/bin/env python2"

srf3:
	# copy schema and related files
	cp fis-oe.mixins/srf/FIS_SCHEMA fis-oe.source/
	# copy python2 pytz package
	rm -rf fis-oe.source/pytz
	rsync --archive fis-oe.mixins/pytz2 fis-oe.source/pytz
	# create new version
	/usr/local/bin/pyzapp create fis-oe.source -f --shebang "/usr/bin/env python3"

whc:
	# copy schema and related files
	cp fis-oe.mixins/whc/FIS_SCHEMA fis-oe.source/
	# copy python2 pytz package
	rm -rf fis-oe.source/pytz
	rsync --archive fis-oe.mixins/pytz2 fis-oe.source/pytz
	# create new version
	/usr/local/bin/pyzapp create fis-oe.source -f --shebang "/usr/bin/env python2"

whc3:
	# copy schema and related files
	cp fis-oe.mixins/whc/FIS_SCHEMA fis-oe.source/
	# copy python2 pytz package
	rm -rf fis-oe.source/pytz
	rsync --archive fis-oe.mixins/pytz2 fis-oe.source/pytz
	# create new version
	/usr/local/bin/pyzapp create fis-oe.source -f --shebang "/usr/bin/env python3"


install-srf:
	# fal-oe
	scp pyzapp.pyz root@fal-oe:/usr/local/bin/pyzapp
	# fal-odoo
	scp pyzapp.pyz root@fal-odoo:/usr/local/bin/pyzapp
	# whc-oe
	scp pyzapp.pyz root@whc-oe:/usr/local/bin/pyzapp

install-whc:
	# fal-oe
	scp pyzapp.pyz root@fal-oe:/usr/local/bin/pyzapp
	# fal-odoo
	scp pyzapp.pyz root@fal-odoo:/usr/local/bin/pyzapp
	# whc-oe
	scp pyzapp.pyz root@whc-oe:/usr/local/bin/pyzapp

update:
	# refreshing dependencies
	for d in aenum antipathy dbf scription stonemark xaml; do echo $$d && rsync --existing /source/virtualenv/lib/py-packages/$$d/* pyzapp/$$d; done

