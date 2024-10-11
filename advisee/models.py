import json

from django.contrib.auth.models import User
from django.db import models

from advisor.models import Advisor

class Advisee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    advisor = models.ForeignKey(Advisor, null=True, on_delete=models.SET_NULL)

    industry = models.TextField(blank=True, null=False, default='')

    # JSON field with this structure, where 1 and 2 are topic ids 
    # {
    #   "1": "some research text that the advisee has written on topic_id:1",
    #   "2": "some research text that the advisee has written on topic_id:2"
    # }
    topic_texts = models.TextField(blank=True, null=False, default='{}')

    # JSON field with this structure, where 1 and 2 are topic ids 
    # {
    #   "1": {
    #           "text": "some instructions that AI generated on topic_id:1",
    #           "unread": "true"
    #        }
    #   "2": {
    #           "text": "some instructions that AI generated on topic_id:2",
    #           "unread": "false"
    #        }
    # }
    topic_instructions = models.TextField(blank=True, null=False, default='{}')

    topic_instructions_default = "AI is generating instructions on how you should approach this topic based on your industry. Please check back later."

    def set_topic_text(self, topic_id, text):
        topic_id = str(topic_id)
        json_obj = json.loads(self.topic_texts)

        json_obj[topic_id] = text.strip()
        self.topic_texts = json.dumps(json_obj)

    def get_topic_text(self, topic_id):
        topic_id = str(topic_id)
        json_obj = json.loads(self.topic_texts)

        if topic_id in json_obj:
            return json_obj[str(topic_id)]
        else:
            return ""

    def set_topic_instruction(self, topic_id, text, unread=True):
        topic_id = str(topic_id)
        unread = "true" if unread else "false"
        text = text.strip()

        json_obj = json.loads(self.topic_instructions)
        
        json_obj[topic_id] = {}
        json_obj[topic_id]["text"] = text
        json_obj[topic_id]["unread"] = unread

        self.topic_instructions = json.dumps(json_obj)

    def get_topic_instruction(self, topic_id):
        topic_id = str(topic_id)
        json_obj = json.loads(self.topic_instructions)

        if topic_id in json_obj:
            instruction = json_obj[topic_id]
            if instruction: 
                return instruction
            else:
                return {"text": self.topic_instructions_default, "unread": "false"}
        else:
            return {"text": self.topic_instructions_default, "unread": "false"}
    
    def mark_topic_instruction_read(self, topic_id):
        topic_id = str(topic_id)
        json_obj = json.loads(self.topic_instructions)

        if topic_id in json_obj:
            json_obj[topic_id]["unread"] = "false"
        
        self.topic_instructions = json.dumps(json_obj)

    