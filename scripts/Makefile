.PHONY: srf srf3 whc whc3

srf:
	# copy schema and related files
	echo data = \"\"\" > fis-oe.source/BBxXlate/schema.py
	cat /opt/FIS/Falcon_FIS_SCHEMA >> fis-oe.source/BBxXlate/schema.py
	echo \"\"\".split\(\"'\\n'\"\) >> fis-oe.source/BBxXlate/schema.py
	cp ./fis_oe_converters.py fis-oe.source/fislib/fis_oe_converters.py
	cp ./fis_schema.py fis-oe.source/fislib/schema.py
	cp ./recipe.py fis-oe.source/fislib/recipe.py
	cp ./updates.py fis-oe.source/fislib/__init__.py
	cp ./updates_mapping.py fis-oe.source/fislib/mapping.py
	
	# copy python2 pytz package
	rm -rf fis-oe.source/pytz
	rsync --archive fis-oe.mixins/pytz2/* fis-oe.source/pytz
	# create new version
	/usr/local/bin/pyzapp create fis-oe.source -f --shebang "/usr/bin/env python2"

srf3:
	# copy schema and related files
	echo data = \"\"\" > fis-oe.source/BBxXlate/schema.py
	cat /opt/FIS/Falcon_FIS_SCHEMA >> fis-oe.source/BBxXlate/schema.py
	echo \"\"\".split\(\"'\\n'\"\) >> fis-oe.source/BBxXlate/schema.py
	cp ./fis_oe_converters.py fis-oe.source/fislib/fis_oe_converters.py
	cp ./fis_schema.py fis-oe.source/fislib/schema.py
	cp ./recipe.py fis-oe.source/fislib/recipe.py
	cp ./updates.py fis-oe.source/fislib/__init__.py
	cp ./updates_mapping.py fis-oe.source/fislib/mapping.py
	# copy python3 pytz package
	rm -rf fis-oe.source/pytz
	rsync --archive fis-oe.mixins/pytz3/* fis-oe.source/pytz
	# create new version
	/usr/local/bin/pyzapp create fis-oe.source -f --shebang "/usr/bin/env python3"

whc:
	# copy schema and related files
	echo data = \"\"\" > fis-oe.source/BBxXlate/schema.py
	cat /opt/FIS/WholeHerb_FIS_SCHEMA >> fis-oe.source/BBxXlate/schema.py
	echo \"\"\".split\(\"'\\n'\"\) >> fis-oe.source/BBxXlate/schema.py
	cp /opt/whc/openerp/addons/wholeherb_integration/scripts/fis_oe_converters.py fis-oe.source/fislib/fis_oe_converters.py
	cp /opt/whc/openerp/addons/wholeherb_integration/scripts/fis_schema.py fis-oe.source/fislib/schema.py
	cp /opt/whc/openerp/addons/wholeherb_integration/scripts/updates.py fis-oe.source/fislib/__init__.py
	cp /opt/whc/openerp/addons/wholeherb_integration/scripts/updates_mapping.py fis-oe.source/fislib/mapping.py
	rm fis-oe.source/fislib/recipe.py
	# copy python2 pytz package
	rm -rf fis-oe.source/pytz
	rsync --archive fis-oe.mixins/pytz2/* fis-oe.source/pytz
	# create new version
	/usr/local/bin/pyzapp create fis-oe.source -f --shebang "/usr/bin/env python2"

whc3:
	# update customer specific files
	echo data = \"\"\" > fis-oe.source/BBxXlate/schema.py
	cat /opt/FIS/WholeHerb_FIS_SCHEMA >> fis-oe.source/BBxXlate/schema.py
	echo \"\"\".split\(\"'\\n'\"\) >> fis-oe.source/BBxXlate/schema.py
	cp /opt/whc/openerp/addons/wholeherb_integration/scripts/fis_oe_converters.py fis-oe.source/fislib/fis_oe_converters.py
	cp /opt/whc/openerp/addons/wholeherb_integration/scripts/fis_schema.py fis-oe.source/fislib/schema.py
	cp /opt/whc/openerp/addons/wholeherb_integration/scripts/updates.py fis-oe.source/fislib/__init__.py
	cp /opt/whc/openerp/addons/wholeherb_integration/scripts/updates_mapping.py fis-oe.source/fislib/mapping.py
	rm fis-oe.source/fislib/recipe.py
	# python3 pytz package
	rm -rf fis-oe.source/pytz
	rsync --archive fis-oe.mixins/pytz3/* fis-oe.source/pytz
	# create new version
	/usr/local/bin/pyzapp create fis-oe.source -f --shebang "/usr/bin/env python3"


install-srf:
	# fal-oe
	scp fis-oe root@fal-oe:/usr/local/bin/fis-oe
	scp fis-oe root@192.168.11.177:/usr/local/bin/fis-oe

install-whc:
	# whc-oe
	scp fis-oe root@whc-oe:/usr/local/bin/fis-oe
	# whca-fis
	scp fis-oe root@192.168.2.2:/usr/local/bin/fis-oe

