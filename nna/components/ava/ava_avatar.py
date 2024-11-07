import bpy

from ...nna_operators_util import CreateNewObjectOperator, SetActiveObjectOperator

from ... import nna_utils_name
from ... import nna_utils_json
from ... import nna_utils_tree


class AddAVAAvatarComponentOperator(bpy.types.Operator):
	"""Specifies this object to be a VR & V-Tubing avatar.
	This component is not nescessary, unless you want to disable on-import-automapping of features.
	"""
	bl_idname = "ava.add_ava_avatar"
	bl_label = "Add AVA Avatar Component"
	bl_options = {"REGISTER", "UNDO"}
	
	target_id: bpy.props.StringProperty(name = "target_id") # type: ignore
	
	def execute(self, context):
		try:
			nna_utils_json.add_component(self.target_id, {"t":"ava.avatar"})
			self.report({'INFO'}, "Component successfully added")
			return {"FINISHED"}
		except ValueError as error:
			self.report({'ERROR'}, str(error))
			return {"CANCELLED"}


class EditAVAAvatarComponentOperator(bpy.types.Operator):
	"""Specifies this object to be a VR & V-Tubing avatar.
	This component is not nescessary, unless you want to disable on-import-automapping of features.
	"""
	bl_idname = "nna.edit_ava_avatar"
	bl_label = "Edit AVA Avatar Component"
	bl_options = {"REGISTER", "UNDO"}

	target_id: bpy.props.StringProperty(name = "target_id") # type: ignore
	component_index: bpy.props.IntProperty(name = "component_index", default=-1) # type: ignore

	automap: bpy.props.BoolProperty(name="Automap", default=True) # type: ignore
	
	def invoke(self, context, event):
		json_component = nna_utils_json.get_component(self.target_id, self.component_index)
		if("auto" in json_component): self.automap = json_component["auto"]
		return context.window_manager.invoke_props_dialog(self)
		
	def execute(self, context):
		try:
			json_component = nna_utils_json.get_component(self.target_id, self.component_index)

			if(not self.automap): json_component["auto"] = False
			elif("auto" in json_component):
				del json_component["auto"]

			nna_utils_json.replace_component(self.target_id, json_component, self.component_index)
			self.report({'INFO'}, "Component successfully edited")
			return {"FINISHED"}
		except ValueError as error:
			self.report({'ERROR'}, str(error))
			return {"CANCELLED"}
	
	def draw(self, context):
		self.layout.prop(self, "automap", expand=True)


def display_ava_avatar_component(object, layout, json_dict):
	autodect = "auto" in json_dict and not json_dict["auto"]
	row = layout.row()
	row.label(text="Automap")
	row.label(text="False" if autodect else "True")

	viewport_object = bpy.data.objects.get("ViewportFirstPerson")
	if(viewport_object):
		row = layout.row()
		row.label(text="Viewport defined by 'ViewportFirstPerson'")
		row.operator(SetActiveObjectOperator.bl_idname).target_name = "ViewportFirstPerson"
	else:
		row = layout.row()
		row.operator(CreateNewObjectOperator.bl_idname, text="Create Viewport Object").target_name = "ViewportFirstPerson"


def name_match_ava_viewport_first_person(name: str) -> int:
	return 0 if name == "ViewportFirstPerson" else -1


nna_types = {
	"ava.avatar": {
		"json_add": AddAVAAvatarComponentOperator.bl_idname,
		"json_edit": EditAVAAvatarComponentOperator.bl_idname,
		"json_display": display_ava_avatar_component,
	},
	"ava.viewport_first_person": {
		"name_match": name_match_ava_viewport_first_person,
	}
}
