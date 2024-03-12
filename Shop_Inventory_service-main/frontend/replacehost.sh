#!/bin/bash

#This file will replace the local host from your code and replace with HOST machine's ip in all the files

sed -i "/usr/share/nginx/html/Employee/Customer&SaleRepot.html" -e 's|localhost|'"$IP_HOST"'|g'
sed -i "/usr/share/nginx/html/Employee/itemsList.html" -e 's|localhost|'"$IP_HOST"'|g'
sed -i "/usr/share/nginx/html/Employee/Billing/SaleReport(Billing).html" 's|localhost|'"$IP_HOST"'|g'
sed -i /usr/share/nginx/html/Manager/createItem.html -e 's|localhost|'"$IP_HOST"'|g'
sed -i /usr/share/nginx/html/Manager/update.html -e 's|localhost|'"$IP_HOST"'|g'
sed -i /usr/share/nginx/html/Manager/viewitems.html -e 's|localhost|'"$IP_HOST"'|g'

nginx -g "daemon off;"
