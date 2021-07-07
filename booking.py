import requests
import urllib
import re
from TeeTime import TeeTime





teeTimeSession = TeeTime()
error_code = ''

# Login
teeTimeSession.post(teeTimeSession.teeTimeUrls["loginURL"],  "login_func")
teeTimeSession.post(teeTimeSession.teeTimeUrls["loginHome"],  "login_func")


# Begin Book Tee Time - this goes to search page 
teeTimeSession.get(teeTimeSession.teeTimeUrls["beginBookTeeTimes"], "bookTeeTimes_func")


# Find times for selected course - iterate through courses until we find one and book a time

for course in teeTimeSession.teeTimeCourses:
	if teeTimeSession.courseSelected:
		break
	data_course = {
		"Date": teeTimeSession.teeTimeDate,
		"SearchTime": teeTimeSession.teeTimeTime,
		"Holes": teeTimeSession.teeTimeHoles,
		"Players": teeTimeSession.teeTimePlayers,
		"CourseId"+course: course,
		"CourseGroupID": "12",
		"Referrer": "www.tee-on.com"
	}
	data_course = '&'.join('{}={}'.format(key, val) for key, val in data_course.items())

	res = teeTimeSession.post(teeTimeSession.teeTimeUrls["bookTeeTimes"], "course_func", data_course)
	# collect list of times available for selected course
	available_times = []
	
	for available_time in teeTimeSession.getTeeTimes(res):
		formatted_time = available_time.text.strip()
		print(int(re.sub(r'[A-Za-z]', '', formatted_time).replace(':', '')))
		print(int(teeTimeSession.teeTimeTime.replace(':', '')))
		if int(re.sub(r'[A-Za-z]', '', formatted_time).replace(':', '')) < int(teeTimeSession.teeTimeTime.replace(':', '')):
			continue
		formatted_time = re.sub(r'[A-Za-z]', '', formatted_time).split(':')
		formatted_time[0] = formatted_time[0].zfill(2)
		formatted_time = ':'.join(formatted_time)

		available_times.append(formatted_time)
		

	if not available_times:
		print("No available time slots for selected configuration, trying next course")
		continue
	
	# Pick a tee time
	
	while available_times:
		data_booking = {
			"CourseCode": course,
			"NineCode": "F",
			"Date": teeTimeSession.teeTimeDate,
			"Time": available_times[0],
			"Holes": teeTimeSession.teeTimeHoles,
			"Players": teeTimeSession.teeTimePlayers,
		}
		data_booking = '&'.join('{}={}'.format(key, val) for key, val in data_booking.items())
		res = teeTimeSession.get(teeTimeSession.teeTimeUrls["checkBookingLock"], "checkBook_func", data_booking)
		if res:
			break
		available_times.pop(0)
	
	data_choosecart = {
		"CourseGroupID": "12",
		"Holes": teeTimeSession.teeTimeHoles,
		"FromSpecials": "false",
		"SearchTime": teeTimeSession.teeTimeTime,
		"ShotgunID": "undefined",
		"Referrer": "www.tee-on.com",
		"CourseId"+course: course,
		"Players": teeTimeSession.teeTimePlayers,
		"BackTarget": "com.teeon.teesheet.servlets.golfersection.WebBookingSearchResults",
		"CourseCode": course,
		"NineCode": "F",
		"Date": teeTimeSession.teeTimeDate,
		"TimeID": "undefined",
		"Time": available_times[0]
	}
	
	data_choosecart = '&'.join('{}={}'.format(key, val) for key, val in data_choosecart.items())
	res = teeTimeSession.post(teeTimeSession.teeTimeUrls["bookingChooseCarts"], "chooseCarts_func", data_choosecart)
	
	if res == None: continue
	
	data_bookcart = {
		"Carts": teeTimeSession.teeTimeCarts,
		#"SearchSubRegion": "LOND",
		"Time": available_times[0],
		"CourseGroupID": "12",
		"Holes": teeTimeSession.teeTimeHoles,
		"FromSpecials": "false",
		"SearchTime": teeTimeSession.teeTimeTime,
		"ShotgunID": "undefined",
		"Referrer": "www.tee-on.com",
		"CourseId "+course: course,
		"Players": teeTimeSession.teeTimePlayers,
		"BackTarget": "com.teeon.teesheet.servlets.golfersection.WebBookingChooseCarts",
		"CourseCode": course,
		"NineCode": "F",
		"Date": teeTimeSession.teeTimeDate,
		"TimeID": "undefined",
		#"UnlockTime1": course + "|F|" + teeTimeSession.teeTimeDate + "|" + available_times[0] + "|" + |B|09:40|18",
		"Ride0": "true",
		"Ride1": "true",
		"Ride2": "false",
		"Ride3": "false",
	}
	
	data_bookcart = '&'.join('{}={}'.format(key, val) for key, val in data_bookcart.items())
	# Pick a cart
	teeTimeSession.post(teeTimeSession.teeTimeUrls["bookingPlayerEntry"], "bookCart_func", data_bookcart)

	# Book Time
	res = teeTimeSession.post(teeTimeSession.teeTimeUrls["bookingBookTime"], "bookTime_func", data_bookcart)
	# print(res)


