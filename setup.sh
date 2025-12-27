#!/bin/bash

CheckVenv()
{
	echo "Checking venv"

	if ! which pip3 >/dev/null 2>/dev/null
	then
		echo "Ensure pip3 is installed and available"
		exit
	fi

	if ! python3 -c "import venv"
	then
		if ! pip3 install --user virtualenv
		then
			echo "Failed to install virtualenv"
			exit
		fi
	fi

	if [ ! -d venv ]
	then
		if ! python3 -m venv venv
		then
			echo "Failed to create venv"
			rm -rf venv
			exit
		fi
	fi

	if ! . ./venv/bin/activate
	then
		echo "Failed to activate venv"
		exit
	fi
}

InstallRequirements()
{
	if ! venv/bin/pip install -r requirements.txt
	then
		exit
	fi
}

CheckVenv
InstallRequirements
