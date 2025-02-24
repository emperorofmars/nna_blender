import json
import bpy

from .utils import nna_utils_tree
from .utils import nna_utils_json
from .utils import nna_kv_list


class SetupNNAMetaOperator(bpy.types.Operator):
	"""Setup NNA Meta Information"""
	bl_idname = "nna.init_meta"
	bl_label = "Setup NNA Meta Information"
	bl_options = {"REGISTER", "UNDO"}

	def execute(self, context):
		root = nna_utils_tree.find_nna_root()
		if(root):
			originalSelectedObject = bpy.context.active_object
			bpy.ops.object.empty_add()
			nnaObject = bpy.context.active_object
			nnaObject.name = "$meta"
			nnaObject.parent = root
			bpy.context.view_layer.objects.active = originalSelectedObject
			self.report({"INFO"}, "NNA Meta successfully created")
			return {"FINISHED"}
		else:
			return {"CANCELLED"}


class EditNNAMetaOperator(bpy.types.Operator):
	"""Edit NNA Meta Information"""
	bl_idname = "nna.edit_meta"
	bl_label = "Edit NNA Meta Information"
	bl_options = {"REGISTER", "UNDO"}

	name: bpy.props.StringProperty(name="Asset Name") # type: ignore
	author: bpy.props.StringProperty(name="Author") # type: ignore
	version: bpy.props.StringProperty(name="Version") # type: ignore
	url: bpy.props.StringProperty(name="Asset Link") # type: ignore
	license: bpy.props.StringProperty(name="License") # type: ignore
	license_url: bpy.props.StringProperty(name="License Link") # type: ignore
	documentation_url: bpy.props.StringProperty(name="Documentation Link") # type: ignore

	# TODO user defined properties

	def invoke(self, context, event):
		meta = nna_utils_tree.determine_nna_meta()
		json_text = nna_utils_json.get_json_from_targeting_object(meta)
		json_meta = json.loads(json_text) if json_text else {}

		if("name" in json_meta): self.name = json_meta["name"]
		if("author" in json_meta): self.author = json_meta["author"]
		if("version" in json_meta): self.version = json_meta["version"]
		if("url" in json_meta): self.url = json_meta["url"]
		if("license" in json_meta): self.license = json_meta["license"]
		if("license_url" in json_meta): self.license_url = json_meta["license_url"]
		if("documentation_url" in json_meta): self.documentation_url = json_meta["documentation_url"]

		if("custom_properties" in json_meta):
			bpy.context.scene.nna_kv_list.clear()
			for key, value in json_meta.get("custom_properties", {}).items():
				new_entry = bpy.context.scene.nna_kv_list.add()
				new_entry.key = key
				new_entry.value = value

		return context.window_manager.invoke_props_dialog(self)

	def execute(self, context):
		try:
			meta = nna_utils_tree.determine_nna_meta()
			json_text = nna_utils_json.get_json_from_targeting_object(meta)
			json_meta = json.loads(json_text) if json_text else {}

			if(self.name): json_meta["name"] = self.name
			elif("name" in json_meta): del json_meta["name"]
			if(self.author): json_meta["author"] = self.author
			elif("author" in json_meta): del json_meta["author"]
			if(self.version): json_meta["version"] = self.version
			elif("version" in json_meta): del json_meta["version"]
			if(self.url): json_meta["url"] = self.url
			elif("url" in json_meta): del json_meta["url"]
			if(self.license): json_meta["license"] = self.license
			elif("license" in json_meta): del json_meta["license"]
			if(self.license_url): json_meta["license_url"] = self.license_url
			elif("license_url" in json_meta): del json_meta["license_url"]
			if(self.documentation_url): json_meta["documentation_url"] = self.documentation_url
			elif("documentation_url" in json_meta): del json_meta["documentation_url"]

			if(bpy.context.scene.nna_kv_list):
				json_meta["custom_properties"] = {}
				for kv_entry in bpy.context.scene.nna_kv_list:
					if(kv_entry.key):
						json_meta["custom_properties"][kv_entry.key] = kv_entry.value
				bpy.context.scene.nna_kv_list.clear()
			elif("custom_properties" in json_meta):
				del json_meta["custom_properties"]

			nna_utils_json.serialize_json_to_targeting_object(meta, json.dumps(json_meta))
			self.report({'INFO'}, "Component successfully edited")
			return {"FINISHED"}
		except ValueError as error:
			self.report({'ERROR'}, str(error))
			return {"CANCELLED"}

	def draw(self, context):
		self.layout.prop(self, "name", expand=True)
		self.layout.prop(self, "author", expand=True)
		self.layout.prop(self, "version", expand=True)
		self.layout.prop(self, "url", expand=True)
		self.layout.prop(self, "license", expand=True)
		self.layout.prop(self, "license_url", expand=True)
		self.layout.prop(self, "documentation_url", expand=True)

		self.layout.separator(factor=0.5)
		self.layout.label(text="Custom Properties")
		nna_kv_list.edit_kv_list(self, context)

