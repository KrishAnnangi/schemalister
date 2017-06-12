from django.db import models


class Schema(models.Model):
	random_id = models.CharField(db_index=True,max_length=255, blank=True)
	created_date = models.DateTimeField(null=True,blank=True)
	finished_date = models.DateTimeField(null=True,blank=True)
	org_id = models.CharField(max_length=255)
	org_name = models.CharField(max_length=255, blank=True)
	username = models.CharField(max_length=255, blank=True)
	access_token = models.CharField(max_length=255, blank=True)
	instance_url = models.CharField(max_length=255, blank=True)
	include_field_usage = models.BooleanField(default=False)
	status = models.CharField(max_length=255, blank=True)
	error = models.TextField(blank=True)

	def sorted_objects(self):
		return self.object_set.order_by('label')

	def sorted_objects_api(self):
		return self.object_set.order_by('api_name')

class Object(models.Model):
	schema = models.ForeignKey(Schema)
	label = models.CharField(max_length=255)
	api_name = models.CharField(max_length=255)

	def sorted_fields(self):
		return self.field_set.order_by('label')


class Field(models.Model):
	object = models.ForeignKey(Object)
	label = models.CharField(max_length=255)
	api_name = models.TextField(max_length=255)
	data_type = models.TextField()
	description = models.TextField(blank=True, null=True)
	help_text = models.TextField(blank=True, null=True)

	def page_layout_usage(self):
		return self.fieldusage_set.filter(type='Page Layout')

	def workflow_usage(self):
		return self.fieldusage_set.filter(type='Workflow')

	def field_update_usage(self):
		return self.fieldusage_set.filter(type='Field Update')

	def email_template_usage(self):
		return self.fieldusage_set.filter(type='Email Template')

	def flow_usage(self):
		return self.fieldusage_set.filter(type='Flow')

	def classes_usage(self):
		return self.fieldusage_set.filter(type='Apex Class')

	def triggers_usage(self):
		return self.fieldusage_set.filter(type='Apex Trigger')

	def components_usage(self):
		return self.fieldusage_set.filter(type='VisualForce Component')

	def pages_usage(self):
		return self.fieldusage_set.filter(type='VisualForce Page')

	def usages(self):
		return self.fieldusage_set.all()


class FieldUsage(models.Model):
	"""
	Captures each location that the field is used in
	"""

	field = models.ForeignKey(Field)

	TYPE_CHOICES = (
		('Apex Class', 'Apex Class'),
		('Apex Trigger', 'Apex Trigger'),
		('Email Template', 'Email Template'),
		('Field Update', 'Field Update'),
		('Page Layout', 'Page Layout'),
		('Flow', 'Flow'),
		('VisualForce Component', 'VisualForce Component'),
		('VisualForce Page', 'VisualForce Page'),
		('Workflow', 'Workflow'),
	)

	type = models.CharField(max_length=50, choices=TYPE_CHOICES)
	name = models.CharField(max_length=255)

	def type_plural(self):
		if self.type == 'Apex Classes':
			return self.type + 'es'
		return self.type + 's'


class Debug(models.Model):
	debug = models.TextField()
