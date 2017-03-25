import json
import sqlite3
from watson_developer_cloud import ConversationV1
import Queue as q


class Chatbot(object):
	"""Chatbot implementation """

	conversation = ConversationV1(
	            username='a8fd0bbc-aaa0-46d6-87d1-0ac0189b7555',
	            password='MfFppOZkLUVO',
	            version='2016-09-20')

	# replace with your own workspace_id
	workspace_id = '92d52185-35fa-4258-b03d-b0098fd5b566'

	def __init__(self):
		self.chatInQ = q.Queue()
		self.chatOutQ = q.Queue()


	def getBalance(accountNo):
		conn = sqlite3.connect('./bank1.db')
		recvdata = conn.execute("select AccountBalance from Accounts where AccountID = " + str(accountNo) + ";")
		bal = 0
		for row in recvdata:
			bal = row[0]

		conn.close()
		return bal

	def sendToChatbot(mesg):
		chatInQ.put(mesg)

	def send_email(account, histnum):
		pass

	def transferFunds(account, recacnt, amnt):
		pass

	def createFD(account, amount):
		pass

	def processResponse(self, response):
		
		category = response['intents'][0]['intent']

		if category == "enquiry":

			self.chatOutQ.put(response['output']['text'][0])
			while(self.chatInQ.empty()):
				#wait here till we get any message
				pass
			account = self.chatInQ.get()
			response = conversation.message(workspace_id=workspace_id, message_input={
			    'text': account}, context=response['context'])

			bal = getBalance(account)
			return response['output']['text'][0] + ' Rs.' + str(bal)

		

		elif category == "send_email":

			self.chatOutQ.put(response['output']['text'][0])
			while(self.chatInQ.empty()):
				#wait here till we get any message
				pass
			account = self.chatInQ.get()
			response = conversation.message(workspace_id=workspace_id, message_input={
			    'text': account}, context=response['context'])
			
			self.chatOutQ.put(response['output']['text'][0])
			while(self.chatInQ.empty()):
				#wait here till we get any message
				pass
			histnum = self.chatInQ.get()
			response = conversation.message(workspace_id=workspace_id, message_input={
			    'text': histnum}, context=response['context'])
			send_email(account, histnum)
			return response['output']['text'][0]

		

		elif category == "transfer":
			
			self.chatOutQ.put(response['output']['text'][0])
			while(self.chatInQ.empty()):
				#wait here till we get any message
				pass
			account = self.chatInQ.get()
			response = conversation.message(workspace_id=workspace_id, message_input={
			    'text': account}, context=response['context'])
			
			self.chatOutQ.put(response['output']['text'][0])
			while(self.chatInQ.empty()):
				#wait here till we get any message
				pass
			recacnt = self.chatInQ.get()
			response = conversation.message(workspace_id=workspace_id, message_input={
			    'text': recacnt}, context=response['context'])
			
			self.chatOutQ.put(response['output']['text'][0])
			while(self.chatInQ.empty()):
				#wait here till we get any message
				pass
			amnt = self.chatInQ.get()
			response = conversation.message(workspace_id=workspace_id, message_input={
			    'text': amnt}, context=response['context'])
			return transferFunds(account, recacnt, amnt)

		

		elif category == "create":
			
			self.chatOutQ.put(response['output']['text'][0])
			while(self.chatInQ.empty()):
				#wait here till we get any message
				pass
			amount = self.chatInQ.get()
			response = conversation.message(workspace_id=workspace_id, message_input={
			    'text': account}, context=response['context'])
			
			self.chatOutQ.put(response['output']['text'][0])
			while(self.chatInQ.empty()):
				#wait here till we get any message
				pass
			amount = self.chatInQ.get()
			response = conversation.message(workspace_id=workspace_id, message_input={
			    'text': amount}, context=response['context'])

			return createFD(account,amount)

		

		else :
			return response['output']['text'][0]



	def startChat(self):
		if(!self.chatInQ.empty()):
			userin = self.chatInQ.get()
			response = conversation.message(workspace_id=workspace_id, message_input={
			    'text': userin})

			pres = processResponse(response)
			# print(json.dumps(response, indent=2))
			# print '#'*20
			self.chatOutQ.put(pres)

			# if response['intents'][0]['intent'] == "sign_off":
				# break

			# When you send multiple requests for the same conversation, include the
			# context object from the previous response.
			# response = conversation.message(workspace_id=workspace_id, message_input={
			# 'text': 'turn the wipers on'},
			#                                context=response['context'])
			# print(json.dumps(response, indent=2))

		return ''