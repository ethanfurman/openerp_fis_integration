.PHONY: srf srf3 whc whc3

srf:
	# copy schema and related files
	rm -rf fis-oe.source/fislib
	rsync --archive /opt/falcon/lib/python2.7/site-packages/fislib fis-oe.source
	echo data = \"\"\" > fis-oe.source/fislib/BBxXlate/schema.py
	cat /opt/falcon/Falcon_FIS_SCHEMA >> fis-oe.source/fislib/BBxXlate/schema.py
	echo \"\"\".split\(\"'\\n'\"\) >> fis-oe.source/fislib/BBxXlate/schema.py
	#
	# copy python2 pytz package
	rm -rf fis-oe.source/pytz
	rsync --archive fis-oe.mixins/pytz2/* fis-oe.source/pytz
	# create new version
	/usr/local/bin/pyzapp create fis-oe.source --force --output fis-oe2 --shebang "/usr/bin/env python2"
	#
	# copy python3 pytz package
	rm -rf fis-oe.source/pytz
	rsync --archive fis-oe.mixins/pytz3/* fis-oe.source/pytz
	# create new version
	/usr/local/bin/pyzapp create fis-oe.source --force --output fis-oe3 --shebang "/usr/bin/env python3"

whc:
	# copy schema and related files
	rm -rf fis-oe.source/fislib
	rsync --archive /opt/whc/lib/python2.7/site-packages/fislib fis-oe.source
	echo data = \"\"\" > fis-oe.source/fislib/BBxXlate/schema.py
	cat /opt/whc/WholeHerb_FIS_SCHEMA >> fis-oe.source/fislib/BBxXlate/schema.py
	echo \"\"\".split\(\"'\\n'\"\) >> fis-oe.source/fislib/BBxXlate/schema.py
	# copy python2 pytz package
	rm -rf fis-oe.source/pytz
	rsync --archive fis-oe.mixins/pytz2/* fis-oe.source/pytz
	# create new version
	/usr/local/bin/pyzapp create fis-oe.source -f --shebang "/usr/bin/env python2"
	#
	# python3 pytz package
	rm -rf fis-oe.source/pytz
	rsync --archive fis-oe.mixins/pytz3/* fis-oe.source/pytz
	# create new version
	/usr/local/bin/pyzapp create fis-oe.source --force --output fis-oe3 --shebang "/usr/bin/env python3"


install-srf:
	# fal-oe
	scp fis-oe2 root@fal-oe:/usr/local/bin/fis-oe
	scp fis-oe3 root@fal-oe:/usr/local/bin/fis-oe3
	scp fis-oe3 root@192.168.11.177:/usr/local/bin/fis-oe3

install-whc:
	# whc-oe
	sudo cp fis-oe /usr/local/bin/whc-fis-oe
	sudo cp fis-oe3 /usr/local/bin/whc-fis-oe3
	scp fis-oe root@whc-oe:/usr/local/bin/fis-oe2
	scp fis-oe3 root@whc-oe:/usr/local/bin/fis-oe
	# whc-fis
	scp fis-oe2 root@192.168.2.2:/usr/local/bin/fis-oe
	scp fis-oe3 root@192.168.2.2:/usr/local/bin/fis-oe3

