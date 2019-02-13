import pymysql
import re
import json
from connection import create_connection, save


def existing_user(user_id):
	connection = create_connection()
	cursor = connection.cursor(pymysql.cursors.DictCursor)
	cursor.execute("SELECT `tm_id` FROM `users` WHERE `tm_id` = "+str(user_id))
	user_id = cursor.fetchone()
	connection.close()

	if user_id:
		return True
	return False



def addlinkDB(link, user_id):
	connection = create_connection()
	cursor = connection.cursor(pymysql.cursors.DictCursor)

	sql = "INSERT INTO `links` (`link`, `tm_id`) VALUES ('"+link.strip()+"', "+str(user_id)+")"
	cursor.execute(sql)
	cursor = connection.cursor()
	connection.commit()
	cursor.close()
	connection.close()