#!/usr/bin/python

# v7(pyAttack) beta by W_G 29/4/2017
# adding fuzzing features
# structs!!
# with response search
# method specific options?

# this interactive program builds fully customizable http requests

# worzel_gummidge

import socket
import sys
import os
import time
import subprocess
import pickle
import errno
import glob
import re

#this is the menu the user will see after execution
def start_options():
        print "What would you like to do?:\n1. Create attack configuration\n2. Use saved configuration\n3. View saved configuration files\n4. Delete configuration file\n5. Clear log file"
        start_option = raw_input()
        if start_option == '1':
                dat = collect_data()
                return dat
        elif start_option == '2':
                dat = retrieve_data()
                return dat
        elif start_option == '3':
                view_conf_files()
                dat = start_options()
                return dat
        elif start_option == '4':
                delete_conf_file()
                dat = start_options()
                return dat
	elif start_option == '5':
		clear_log()
	        exit(0)	
        else:
                print "[!]Invalid selection"
                return start_options()

#this is an interactive function that collects data from the user. This data will be used to create requests and configure request parameters
def collect_data():
        headers = []
        p = 0
        params = []
        print "[+]Enter Attack Configuration\n\n"
        print "[*]Please enter Hostname (e.g. google.com):"
        host = raw_input()
        print "[*]Please enter TCP port:"
        port = raw_input()
        try:
                if int(port) < 0 or int(port) > 65535:
                        print "[!]Invalid port number. Please select a number between 0 and 65535:"
                        new_port = raw_input()
                        port = new_port
                        if int(port) < 0 or int(port) > 65535:
                                print "[!]Invalid port number. Terminating.."
                                exit(1)
	except ValueError:
                print "[!]Invalid port number. Terminating.."
                exit(1)
        print "[*]Please enter URL(without parameters):"
        url = raw_input()
        add = add_param()
        p += add[0]
        params += add[1]
        print "[*]Please enter method (GET,POST etc.):"
        method = raw_input().upper()
        headers += add_headers()
        print "[*]HTTP version?:"
        version = raw_input()

        return (method, url, host, p, params, port, headers, version)

#this function adds and configures parameters
def add_param():
	print "[+]Would you like to add parameters to your request (y/n)?"
	add_params = raw_input()

	params = []
	if add_params == 'y':
		i = 0
		while i >= 0:
			print "[+]Enter Parameter Details\n\n"
			print "[*]Name of parameter:"
			params += [{'name':'', 'value':'', 'type':'', 'modify':''}]
			params[i]['name'] = raw_input()
			print "[*]Value of parameter:"
			params[i]['value'] = raw_input()
			print "[*]Parameter type (1:url, 2:cookie, 3:body) enter relevant number:"
			try:
				params[i]['type'] = raw_input()
				if int(params[i]['type']) <= 0 or int(params[i]['type']) > 3:
					print "[!]Invalid selection, please pick a number between 1 and 3"
					return add_param()
			except ValueError:
				print "[!]Invalid selection, please pick a number between 1 and 3"
				return add_param()

			print "[*]Modify parameter (y/n)?:"
			params[i]['modify'] = raw_input().lower()
			if params[i]['modify'] != 'y'and params[i]['modify'] != 'n':
				print "[!]Invalid selection, please select 'y' for YES and 'n' for NO"
				return add_param()

			print "[*]Add another parameter? (y/n):"
			another_param = raw_input().lower()
			if another_param == 'y':
				i += 1
			elif another_param == 'n':
				p = i
				i = -1
			else:
				print "[!]Invalid selection, please select 'y' for YES and 'n' for NO"
				return add_param()
	elif add_params == 'n':
		p = -1
		params = []
	else:
		print "[!]Invalid selection, please select 'y' for YES and 'n' for NO\n"
		p = add_param()[0]
	return (p, params)

#this function adds headers to the request
def add_headers():
        headers = [{'Name':'User-Agent', 'Value':'Mozilla/5.0 (X11; Linux i686; rv:31.0)', 'Position':'1'}, {'Name':'Accept', 'Value':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Position':'1'}, {'Name':'Accept-Language', 'Value':'en-US,en;q=0.5', 'Position':'1'}, {'Name':'Connection', 'Value':'Keep-Alive', 'Position':'1'}]

        print "[*]Would you like to use the default headers below (y/n)?"
        print "User-Agent: Mozilla/5.0 (X11; Linux i686; rv:31.0)\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'\nAccept-Language: en-US,en;q=0.5\nConnection: Keep-Alive\n"
        default_headers = '1'
        while default_headers != '0':
                default_headers = raw_input()
                if default_headers == 'y':
                        return headers
                elif default_headers == 'n':
                        edit_headers(headers)
                        return headers
                else:
                        print "[!]Invalid selection, please select 'y' for YES and 'n' for NO\n"
			return add_headers()

#this function takes the request headers as an argument. It lets the user customize the headers
def edit_headers(headers):
        print "[*]What would you like to do?\n1. Add a header\n2. Remove a header\n3. Modify a header's value\n4. Accept changes and return"
        edit_header = raw_input()
        if edit_header == '1':
                print "Please enter header name:"
                header_name = raw_input()
                print "Please enter header value:"
                header_value = raw_input()
                headers += [{'Name':header_name, 'Value':header_value, 'Position':'1'}]
                edit_headers(headers)

        elif edit_header == '2':
                print "\n"
                h = 1
                for header in headers:
			print str(h + 1) + ". " + headers[h]['Name'] + ": " + headers[h]['Value']
                        h += 1
                print "\n[*]Please select the number of the header you would like to remove:"
                index = int(raw_input()) - 1
                if index <= (len(headers)-1):
                        del headers[index]
                        edit_headers(headers)
                else:
                        print "[!]Invalid selection"
                        edit_headers()
	elif edit_header == '3':
                print "\n"
                h = 0
                for header in headers:
                        print str(h + 1) + ". " + headers[h]['Name'] + ": " + headers[h]['Value']
                        h += 1
                print "\n[*]Please select the number of the header you would like to modify:"
                index = int(raw_input()) - 1
                if index <= (len(headers)-1):
                        print "[*]Please enter new header value:"
                        new_header_value = raw_input()
                        headers[index]['Value'] = new_header_value
                        edit_headers(headers)
                else:
                        print "[!]Invalid selection"
                        edit_headers()

        elif edit_header == '4':
                return headers
	else:
                print "[!]Invalid response"
                edit_headers(headers)

#this function retirves previously saved data from within the save file
def retrieve_data():
        print "[*]Please enter the name of the saved file (without file path and extension):"
        filename = raw_input()
        filename = '/usr/share/bob/' + filename + '.dat'
        try:
                file_desc = open(filename, 'r')
        except IOError:
                print "[!]Failed to read file %s" %filename
                exit(0)
        data = pickle.load(file_desc)
        file_desc.close()
	method = data[0]
        url = data[1]
        host = data[2]
        p = data[3]
        params = data[4]
        port = data[5]
        headers = data[6]
        version = data[7]
	try:
	        directory_1 = "/tmp/bob/"
        	os.mkdir(directory_1)
	except OSError:
                pass
	try:
        	directory_2 = "/tmp/bob/" + host
        	os.mkdir(directory_2)
	except OSError:
        	pass

        return data

#this function displays the saved files within the save folder
def view_conf_files():
        directory = '/usr/share/bob/'
        path = directory + '*.dat'
        try:
                files =  glob.glob(path)
                for item in files:
                        print item

        except OSError:
                print "[!]Failed to list contents of %s" %directory
                exit(0)
        print "\n"

#this function deletes configuration files
def delete_conf_file():
        print "[*]Please enter filename (without path):"
        filename = raw_input()
        filename = '/usr/share/bob/' + filename
        try:
                os.remove(filename)
        except OSError:
                print "[!]Failed to delete file %s" %filename
                exit(0)

#this function recieves data(configuration) taken from the collect_data functionand gives the user options on how to use this data. It controls the flow of the program and serves as the main menu
def options(data):
	method = data[0]
	url = data[1]
	host = data[2]
	p = data[3]
	params = data[4]
	port = data[5]
	headers = data[6]
	version = data[7]

        show = build_request(method, url, host, p, params, headers, version)
        print "\n\n" + show
	print "\n[+]What would you like to do?\n 1. Re-configure attack details- rebuilds request\n 2. Send the request - sends the current request\n 3. Import a list\n 4. Modify the parameters - attach a payload to a parameter\n 5. Modify the url - attach a url payload\n 6. Modify headers - add, delete, modify a header's value or attach a header payload\n 7. Modify Method - modifies the HTTP Method method\n 8. Modify HTTP version - attach a payload to modify the HTTP version\n 9. Search for a String within the Response\n10. Save current configuration for later use\n99. Exit - quits the application"
        option_1 = raw_input()
	if option_1 == '1':
		data = collect_data()
		options(data)
        elif option_1 == '2':
                response = send_request(show, host, port)
                print "\nURL\t\tStatus\tLength"
                print "===\t\t======\t======"
                report(response, url, p, params, method, host, port, 2)
                print "\n[*]Would you like to:\n0. Return to main menu?\n1. View the response headers?\n2. View the page in Firefox browser?\n3. Search for string in response\n99. Exit the application?"
                option_2 = raw_input()
 		print "\n"
		if option_2 == '0':
                        options(data)
                elif option_2 == '1':
			html = '/tmp/bob/' + host + '/response.html'
			header_file_desc = open(html, "w")
			header_file_desc.write(response)
			time.sleep(2)
			header_file_desc.close()
                        print_header(response)
			print "\nWould you like to view the page in Firefox browser (y/n)?"
			view_html_page = raw_input()
                        if view_html_page == 'y':
                                subprocess.call(['firefox', html, '&'])
                                options(data)
                        elif view_html_page == 'n':
                                options(data)
                        else:
                                print "Invalid response. Type 'y' for YES and 'n' for NO\n"
                                options(data)

                elif option_2 == '2':
			html = '/tmp/bob/' + host + '/response.html'
	                header_file_desc = open(html, "w")
        	        header_file_desc.write(response)
                	time.sleep(2)
                	header_file_desc.close()

			subprocess.call(['firefox', html, '&'])
                        print "Would you like to view the response headers (y/n)?"
			view_response_headers = raw_input()
			if view_response_headers == 'y':
				print "\n"
				print_header(response)
				options(data)
			elif view_response_headers == 'n':
				options(data)
			else:	
				print "Invalid response. Type 'y' for YES and 'n' for NO\n"
				options(data)
		elif option_2 == '3':
			search_for_string(response)
			options(data)
		elif option_2 == '99':
			exit()
                else:
                        print "Invalid response. Type 'y' for YES and 'n' for NO\n"
			options(data)
        elif option_1 == '3':
                import_list(data)
		options(data)
	elif option_1 == '4':
                param_payload(data)
		options(data)
        elif option_1 == '5':
                url_payload(data)
		options(data)
        elif option_1 == '6':
		header_payload(data)
		options(data)
	elif option_1 == '7':
		method_payloads(data)
		options(data)
	elif option_1 == '8':
                http_version_options(data)
                options(data)
	elif option_1 == '9':
                search_for_string(data)
                options(data)
	elif option_1 == '10':
		save_configuration(data)
		options(data)
	elif option_1 == '11':
		clear_log()
		options(data)
        elif option_1 == '99':
                exit(99)
        else:
                print "[!]Invalid selection\n"
                options(data)

#this function takes the method - http method, url, host, p - last parameter index, param - request parameters and headers - request headers as arguments. It builds an http request from user specified input
def build_request(method, url, host, p, params, headers, version):
        request = ""
        build_url = ""
        build_cookie = ""
        build_body = ""
        url_param = ""
        cookie_param = ""
        body_param = ""
        i = c = 0
#deleting headers to avoid dups from previous build
	for header in headers:
		if headers[i]['Position'] == '2':
			del headers[i]
		i += 1
	i = 0
	for header in headers:
		if headers[i]['Position'] == '2':
			del headers[i]
		i += 1
	i = 0
	for header in headers:
		if headers[i]['Position'] == '2':
			del headers[i]
		i += 1
        i = 0
#url
        for parameter in params:
                if params[i]['type'] == '1':
                        c += 1
                        url_param += params[i]['name'] + "=" + params[i]['value'] + "&"
                i += 1
        i = 0
	if p > 0:
		if c > 0:
                	build_url = url + url_param[0:(len(url_param)-1)]
        	else:
                	build_url = url
	else:
		build_url = url
        c = 0
#cookie
        for parameter in params:
                if params[i]['type'] == '2':
                        c += 1
                        cookie_param += params[i]['name'] + "=" + params[i]['value'] + ";"
                i += 1
        i = 0
	if c > 0:
                build_cookie = cookie_param[0:(len(cookie_param)-1)]
                headers += [{'Name':'Cookie', 'Value':build_cookie, 'Position':'2'}]
        c = 0
#body
        for parameter in params:
                if params[i]['type'] == '3':
                        c += 1
                        if params[i]['value'] == '':
                            body_param += params[i]['name']     # parameter has no value
                        else:
                            body_param += params[i]['name'] + "=" + params[i]['value'] + ";"
                i += 1
        i = 0
        if c > 0:
                build_body = body_param[0:(len(body_param)-1)]
                headers += [{'Name':'Content-Type', 'Value':'application/x-www-form-urlencoded', 'Position':'2'}]
                headers += [{'Name':'Content-Length', 'Value':str(len(build_body)), 'Position':'2'}]


        request += method + " " + build_url + " " + "HTTP/" + version + "\r\n" + "Host: " + host + "\r\n"
	for header in headers:
                request += headers[i]['Name'] + ": " + headers[i]['Value'] + "\r\n"
                i += 1
        request += "\r\n" + build_body + "\r\n\r\n"
        return request

#this function takes a request, host and port number as arguments. Its Creates a socket, sends the request, accepts the response and write the repone as text and html files
def send_request(request, host, port):
	log_list = []
        try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((host, int(port)))
                sock.send(request)
                response = sock.recv(20480)
		if check_3xx(response) != 0:		# if we get redirected
			build_request(method, new_url, host, p, params, headers, version)						# got to redirection
			send_request(request, host, port)
			report(response, new_url, p, params, method, host, port, id)
                sock.close()
		log_list += request
		log_list += response
		log(log_list)
                return response
        except socket.gaierror:
		log_list += request				# log in error
		log(log_list)
                print "\n\n\n[!]Error: Please check connectivity\n"
                return "00000000000000"
        except socket.error:
		log_list += request
		log(log_list)
                print "\n\n\n[!]Error: No route to host\n"
                return "00000000000000"

#this function checks whether the http response code is 3xx. if it is, it asks whether the user wants to follow the redirect
def check_3xx(response):
	for line in response:
		if line[10:1] == '3':
			for header in headers:
				if header[0:9] == 'Location:':
					new_url = header[9:]
					return new_url
				else:
					pass
		else:
			pass
	return 0

#this function creates log entries
def log(list):
	buffer = ''
	i = 0
	buffer += "\n--------------------------------------------------------------------------------"
	buffer += "Date: " + time.strftime("%d/%m/%Y") + "\tTime: " + time.strftime("%H:%M:%S")
	buffer += "\n--------------------------------------------------------------------------------"
	for item in list:
		buffer += list[i]
		i += 1
	fdesc = open('/var/log/bob.log', 'a')
	fdesc.write(buffer)
	fdesc.close

#this function takes the response from send_request, the url, p - last parameter index, params - request parameters and id - an identifier to which format to print out as arguments. It prints results of payloads to stdout
def report(response, url, p, params, method, host, port, id):
	if id == 1:
		log = params[p]['name'] + "\t\t" + params[p]['value'] + "\t" + response[9:12] + "\t" + str(len(response))
		print log
	elif id == 2:
		log = url + "\t\t" + response[9:12] + "\t" + str(len(response))
		print log
	elif id == 3:
		log = method + "\t\t" + response[9:12] + "\t" + str(len(response))
		print log
	elif id == 4:
                log = host + "\t\t" + response[9:12] + "\t" + str(len(response))
                print log
	elif id == 5:
                log = port + "\t\t" + response[9:12] + "\t" + str(len(response))
                print log
	elif id == 6:
                log = version + "\t\t" + response[9:12] + "\t" + str(len(response))
                print log
	return log

#this function takes the response from the http request, creates a file(/tmp/'host'response.txt), writes the response to this file and prints out the response headers to stdout
def print_header(response):
	file = '/tmp/bob/' + host + '/response.html'
	for line in open(file):
		if line != '\r\n':
			print line.strip()
		else:
			print '\n'
			return 0

#this function performs a string search in the response
def search_for_string(response):
        print "[+]Please enter search string(python regex supported):"
        search_string = raw_input()
        try:
		pattern = re.compile(search_string)
	except:
		print "[!]Invalid search string"
		return
        if pattern.search(response):
                print "[!]Match found!"
	else:
		print "[!]No match found!"

#this function import a list of modifiable data
def import_list(data):
	print "[+]Import as(?):\n0. Back - Return to the Main Menu\n1. Target Hostname - import a list of target hostnames\n2. Port Number - import a list of port numbers\n3. Relative URL - import a list of relative urls\n4. HTTP Version - import a list of http versions\n99. Exit - quit the application"
	import_as = raw_input()
	if import_as == '0':
		return
	elif import_as == '1':
		target_hostname_list(data)
		options(data)
	elif import_as == '2':
		port_number_list(data)
		options(data)
	elif import_as == '3':
		relative_url_list(data)
		options(data)
	elif import_as == '4':
		http_version_list(data)
		options(data)
	elif import_as == '99':
		exit(0)
	else:
		print "[!]Invalid Selection.."
		return

#this function 
def target_hostname_list(data):
	method = data[0]
        url = data[1]
	host = data[2]
        p = data[3]
        params = data[4]
        port = data[5]
        headers = data[6]
        version = data[7]

	top_5 = []
	file_descriptor = read_from_file()
	print "Host\t\tStatus\t\tLength"
        print "====\t\t======\t\t======"
	for line in file_descriptor:
		host = line.strip()
		request = build_request(method, url, host, p, params, headers, version)
		response = send_request(request, host, port)
		report(response, url, p, params, method, host, port, 4)
#		top_5 += sort_top_5_by_length(response)
#	show_top_5(top_5)

#this function reads from a given file
def read_from_file():
	print "[+]Please enter file name(with full file path and extension)"
	filename = raw_input()
	try:
                file_desc = open(filename, 'r')
		return file_desc
        except Exception as im:
		print im
		file_desc = read_from_file()
		return file_desc

def port_number_list(data):
	method = data[0]
        url = data[1]
        host = data[2]
        p = data[3]
        params = data[4]
        port = data[5]
        headers = data[6]
        version = data[7]

        file_descriptor = read_from_file()
        print "Port\t\tStatus\t\tLength"
        print "====\t\t======\t\t======"
        for line in file_descriptor:
                port = line.strip()
                request = build_request(method, url, host, p, params, headers, version)
                response = send_request(request, host, port)
                report(response, port, p, params, method, host, port, 5)

def relative_url_list(data):
	
	method = data[0]
        url = data[1]
        host = data[2]
        p = data[3]
        params = data[4]
        port = data[5]
        headers = data[6]
        version = data[7]

        file_descriptor = read_from_file()
        print "URL\t\tStatus\t\tLength"
        print "===\t\t======\t\t======"
        for line in file_descriptor:
                url = line.strip()
                request = build_request(method, url, host, p, params, headers, version)
                response = send_request(request, host, port)
                report(response, url, p, params, method, host, port, 2)

def http_version_list(data):
	method = data[0]
        url = data[1]
        host = data[2]
        p = data[3]
        params = data[4]
        port = data[5]
        headers = data[6]
        version = data[7]

        file_descriptor = read_from_file()
        print "HTTP Version\t\tStatus\t\tLength"
        print "============\t\t======\t\t======"
        for line in file_descriptor:
                version = line.strip()
                request = build_request(method, url, host, p, params, headers, version)
                response = send_request(request, host, port)
                report(response, version, p, params, method, host, port, 6)

#this function takes the method - http method, url, host, p - last parameter index, param - request parameters, port and headers - request headers as arguments.It serves as a menu for parameter payloads
def param_payload(data):
        method = data[0]
        url = data[1]
        host = data[2]
        p = data[3]
        params = data[4]
        port = data[5]
        headers = data[6]
        version = data[7]
	print "[+]Enter Payload Details\n\n"

        number_of_params = p + 1

        while number_of_params > 0:
                if params[p]['modify'] == 'y':
                        print "[*]Please select payload for parameter:" + str(params[p]) + "\n0. Main Menu - returns to main menu\n1. Number Iterator - cycles through a set range of numbers\n2. Dictionary Iterator - cycles through enrties from a user supplied file\n99. Exit - quits the application"
                        p_payload = raw_input()
                        if p_payload == '0':
                                return
                        elif p_payload == '1':
                                number_iterator(data)
                                return 0
			elif p_payload == '2':
                                dictionary_iterator(data)
                                return 0
                        elif p_payload == '99':
                                print "Terminating.."
                                exit(99)
                        else:
                                print "[!]Invalid response"
                                return 0

                p -= 1
                number_of_params = p + 1

        print "No parameters to modify!\n"
        return 0

#this function is a payload that traverses through a list of numbers set by max and min values
def number_iterator(data):
	method = data[0]
        url = data[1]
        host = data[2]
        p = data[3]
        params = data[4]
        port = data[5]
        headers = data[6]
        version = data[7]
        print "[*]Please enter starting number:"
        first = raw_input()
        print "[*]Please enter last number:"
        last = raw_input()
        if int(last) < int(first):
                print "[!]Invalid input. Please enter a number greater than the starting number"
                return 0
        print "[*]Please enter step:"
        step = raw_input()
        if (int(last)- int(first)) < int(step) < 1:
                print "[!]Invalid input. Step must be a positive number greater than 0"
                return 0

        print "\n\nParameter\t\tPayload\tStatus\tLength"
        print "=========\t\t=======\t======\t======"

        current = int(first)
        params[p]['value'] = str(current)
        request = build_request(method, url, host, p, params, headers, version)
        response = send_request(request, host, port)
	log_entry = str(report(response, url, p, params, method, host, port, 1))
        while current < int(last):
                current += int(step)
                params[p]['value'] = str(current)
                request = build_request(method, url, host, p, params, headers, version)
		response = send_request(request, host, port)
                report(response, url, p, params, method, host, port, 1)

        print "\nDone!..\n"

#this function iterates through a user supplied dictionary file and replaces the parameter value before sending th request
def dictionary_iterator(data):
	method = data[0]
        url = data[1]
        host = data[2]
        p = data[3]
        params = data[4]
        port = data[5]
        headers = data[6]
        version = data[7]

        file_desc = read_text_file_by_line()

        print "\n\nParameter\tPayload\tStatus\tLength"
	print "=========\t=======\t======\t======"

        for line in file_desc:
                current = line.strip()
                params[p]['value'] = current
                request = build_request(method, url, host, p, params, headers, version)
                response = send_request(request, host, port)
                report(response, url, p, params, method, host, port, 1)

        print "\nDone!..\n"
        return 0

#this function takes the host, p - last parameter index, params - request parameters, port and headers as arguments. It serves as a menu with options to url paylaods.
def url_payload(data):
	method = data[0]
        url = data[1]
        host = data[2]
        p = data[3]
        params = data[4]
        port = data[5]
        headers = data[6]
        version = data[7]
        print "Please select payload:\n0. Main Menu - returns to main menu\n1. Brute Robot - requests for urls from 'Disallowed'in the robots.txt file\n2. Path Traversal - modifies the url with appropriate path traversal sequences (url*sequence*url)\n99. Exit - quits the application"
        u_payload = raw_input()
        if u_payload == '0':
                return 0
        elif u_payload == '1':
                brute_robot(host, p, params, port, headers, version)
                return 0
        elif u_payload == '2':
                path_traversal(data)
                return 0
        elif u_payload == '99':
                print "Terminating.."
                exit(99)
        else:
		print "[!]Invalid selection\n"
                return 0

#this function takes the host, p - last parameter index, params - request parameters, port and headers as arguments. It requests for the /robots.txt file, writes the file in /tmp/'host'/robots.txt, requests each disallowed url and prints out the requested url, status code and length of response to stdout.
def brute_robot(host, p, params, port, headers, version):
	try:
		url = "/robots.txt"
		method = "GET"
		p = -1
		request = build_request(method, url, host, p, params, headers, version)
		response = send_request(request, host, port)
		if response != "00000000000000":
			file = "/tmp/bob/" + host + "/robots.txt"
			try:
				file_desc = open(file, "w")
			except IOError:
				print "[!] Error! Could not open file for writing."
				return
			file_desc.write(response)
			print "[!]Downloading robots.txt"
			time.sleep(2)
			file_desc.close()
			print "URL\t\tStatus\t\tLength"
	        	print "===\t\t======\t\t======"
			for line in open(file):
				if line[0:11] == 'Disallow: /':
					url = line[10:].strip()
					request = build_request(method, url, host, p, params, headers, version)
					response = send_request(request, host, port)
					report(response, url, p, params, method, host, port, 2)
			print "[!]robots.txt file has been downloaded to /tmp/'hostname'/"
		else:
			return 0
	except OSError:
		print "[!]The robots.txt file already exists. Delete the file and folder at /tmp/'host name'/ if you want to re-run the payload"
	return 0

#this funtion gives options to manipulate headers
def header_payload(data):
	method = data[0]
        url = data[1]
        host = data[2]
        p = data[3]
        params = data[4]
        port = data[5]
        headers = data[6]
        version = data[7]
	print "[*]What would you like to do?\n0. Main Menu - returns to main menu\n1. Modify headers manually?\n2. Attach a payload?\n99. Exit - quits the application"
	modify_headers = raw_input()
	if modify_headers == '0':
		options(data)
	elif modify_headers == '1':
		edit_headers(headers)
		options(data)
	elif modify_headers == '2':
		header_payload(data)
		options(data)
	elif modify_headers == '99':
		exit(0)
	else:
		print "[!]Invalid selection\n"
		options(data)

#this payload send path traversal sequences to the server
def path_traversal(data):
	method = data[0]
        url = data[1]
        host = data[2]
        p = data[3]
        params = data[4]
        port = data[5]
        headers = data[6]
        version = data[7]
        sequences = ["/..", "%2f%2e%2e", "%u2216%u002e%u002e", "%252f%252e%252e", "\..", "%5c%2e%2e", "%u2216%u002e%u002e", "%255c%252e%252e"]

        print "URL\t\tStatus\t\tLength"
        print "===\t\t======\t\t======"
	p = -1
	for sequence in sequences:
                modified_url = url + sequence + url
                request = build_request(method, modified_url, host, p, params, headers, version)
                response = send_request(request, host, port)
                report(response, modified_url, p, params, method, host, port, 2)

#this function offers the user payloadds for methods
def method_payloads(data):
        method = data[0]
        url = data[1]
        host = data[2]
        p = data[3]
        params = data[4]
        port = data[5]
        headers = data[6]
        version = data[7]
	print "[*]Select payload number:\n0. Main Menu\n1. Accepted Methods\n99. Exit - quits the application"
        h_payload = raw_input()
        if h_payload == '0':
                return
        elif h_payload == '1':
                accepted_methods(data)
                return 0
        elif h_payload == '99':
                exit(0)
        else:
                print "[!]Invalid option"
		return

#this function fetches the methods accepted by the server
def accepted_methods(data):
        method = data[0]
        url = data[1]
        host = data[2]
        p = data[3]
        params = data[4]
        port = data[5]
        headers = data[6]
        version = data[7]
	methods = ['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT', 'COPY', 'MOVE', 'SEARCH', 'PROPFIND']
        request = build_request(method, url, host, p, params, headers, version)
        response = send_request(request, host, port)
        for line in response:
                if line[0:5] == 'Allow':
                        print "Server Response to OPTIONS = "
                        print line
        print "Method\t\tStatus\t\tLength"
        print "======\t\t======\t\t======"
        i = 0
        for method in methods:
                request = build_request(methods[i], url, host, p, params, headers, version)
                response = send_request(request, host, port)
                report(response, url, p, params, methods[i], host, port, 3)
                i += 1

#this function gives the user options over the http version
def http_version_options(data):
	method = data[0]
        url = data[1]
        host = data[2]
        p = data[3]
        params = data[4]
        port = data[5]
        headers = data[6]
        version = data[7]
	print "[*]Please select option:\n0. Main Menu\n1. Fuzz HTTP version - replaces the HTTP version with malformed data in an attemp to destablize the server\n2. Iterate through list in file - accepts a file from the user and iterates through the file one line at a time\n99. Exit - quits the application"
	http_verion_option = raw_input()
	if http_verion_option == '0':
		return
	elif http_verion_option == '1':
		http_version_fuzz(data)
		return 0
	elif http_verion_option == '2':
		http_version_iterator()
		return 0
	elif http_verion_option == '99':
		exit(0)
	else:
		print "[!]Invalid option. Terminating.."
		exit(1)

#this function fuzzes the http version
def http_version_fuzz(data):
	method = data[0]
        url = data[1]
        host = data[2]
        p = data[3]
        params = data[4]
        port = data[5]
        headers = data[6]
        version = data[7]
	heuristics = []
	integer = 4294967279
	while integer <= 4294967311:
		heuristics.append(integer)
		integer += 1
	integer = (4294967278 / 2)
	while integer <= (4294967312 / 2):
		heuristics.append(integer)
		integer += 1
	integer = (4294967277 / 3)
	while integer <= (4294967313 / 3):
		heuristics.append(integer)
		integer += 1
	integer = (4294967280 / 4)
	while integer <= (4294967312 / 4):
		heuristics.append(integer)
		integer += 1
	integer = 65519
	while integer <= 65551:
		heuristics.append(integer)
		integer += 1
	integer = 65520 / 2
	while integer <= 65550 / 2:
		heuristics.append(integer)
		integer += 1
	integer = 65520 / 3
	while integer <= 65553:
		heuristics.append(integer)
		integer += 1
	integer = (655316) / 4
	while integer <= 65552:
		heuristics.append(integer)
		integer += 1
	integer = 239
	while integer <= 271:
		heuristics.append(integer)
		integer += 1
	integer = 238 / 2
	while integer <= 278:
		heuristics.append(integer)
		integer += 1
	integer = 237 / 3
	while integer <= 279:
		heuristics.append(integer)
		integer += 1
	integer = 236 / 4
	while integer <= 280:
		heuristics.append(integer)
		integer += 1
	print heuristics
#	add threads for speed

def save_configuration(data):
	method = data[0]
        url = data[1]
        host = data[2]
        p = data[3]
        params = data[4]
        port = data[5]
        headers = data[6]
        version = data[7]
	print "\nFile name:"
	filename = raw_input()
	filename = '/usr/share/bob/' + filename + '.dat'
	print "[!]Saving attack configuration.."

	file_desc = open(filename, 'w')
	pickle.dump(data, file_desc)
	file_desc.close()
	print "[!]Configuration saved"

#this function clears the log
def clear_log():
	try:
		os.remove("/var/log/bob.log")
		print "[!]Log file deleted.."
		return
	except OSError as exception:
		if exception.errno != errno.ENOENT:
			raise
		else:
			print "[!]File already deleted.."

			###main function###
program_file = "/usr/share/bob/"
try:
	os.makedirs(program_file)
except OSError as exception:
	if exception.errno != errno.EEXIST:
		raise

data = start_options()

method = data[0]
url = data[1]
host = data[2]
p = data[3]
params = data[4]
port = data[5]
headers = data[6]
version = data[7]

try:
	directory_1 = "/tmp/bob/"
	os.mkdir(directory_1)
	directory_2 = "/tmp/bob/" + host
	os.mkdir(directory_2)
except OSError:
	pass
options(data)
