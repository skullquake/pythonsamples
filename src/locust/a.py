from locust import HttpLocust, TaskSet, task
class UserBehavior(TaskSet):
	def on_start(self):
		"""
		"""
		self.getSession()
		self.login()
	def on_stop(self):
		"""
		"""
		self.logout()
	def getSession(self):
		self.client.headers['Content-Type']="application/json"
		response=self.client.post(
			"/xas/",
			json={
				"action":"get_session_data",
				"params":{
					"path":"."
				}
			}
		)
		self.token=response.json()['csrftoken']
	def login(self):
		self.client.headers['Content-Type']='application/json'
		self.client.headers['X-Csrf-Token']=self.token;
		response=self.client.post(
			'/xas/',
			json={
				"action":"login",
				"params":{
					"username":"MxAdmin",
					"password":"1234!@#$qwerQWER"
				},
			}
		)
		self.token=response.json()['csrftoken']
	def logout(self):
		self.client.headers['Content-Type']='application/json'
		self.client.headers['X-Csrf-Token']=self.token;
		response=self.client.post(
			"/xas/",json={
				"action":"logout",
				"params":{
				}
			}
		)
	@task(1)
	def retrieve(self):
		self.client.headers['Content-Type']='application/json'
		self.client.headers['X-Csrf-Token']=self.token;
		response=self.client.post(
			'/xas/',
			json={
				"action":"retrieve_by_xpath",
				"params":{
					"xpath":"//Module.Entity[attr='val'] [attr2='val2']",
					"schema":{
						"sort":[
							[
								"attr3","desc"
							]
						],
						"offset":0,
						"amount":8
					},
					"count":True
				}
			}
		)
class WebsiteUser(HttpLocust):
	task_set=UserBehavior
	min_wait=5000
	max_wait=9000
