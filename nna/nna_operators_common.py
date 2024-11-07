import bpy
from . import nna_utils_tree
from . import nna_utils_json
from . import nna_utils_name


class InitializeNNAOperator(bpy.types.Operator):
	"""Creates the root `$nna` object in the scene.
	If the `nna_init_collection` property is set, it will create it in that collection.
	"""
	bl_idname = "nna.init"
	bl_label = "Initialize NNA in Active Collection"
	bl_options = {"REGISTER", "UNDO"}

	nna_init_collection: bpy.props.StringProperty(name = "nna_init_collection") # type: ignore
	
	def execute(self, context):
		if bpy.context.scene.collection.name == self.nna_init_collection or not self.nna_init_collection:
			nna_utils_tree.init_nna_root(bpy.context.scene.collection)
			self.report({"INFO"}, "NNA inited in Scene Collection")
			return {"FINISHED"}
		else:
			for collection in [bpy.context.scene.collection, *bpy.context.scene.collection.children_recursive]:
				if(collection.name == self.nna_init_collection):
					nna_utils_tree.init_nna_root(collection)
					self.report({"INFO"}, "NNA inited in " + collection.name)
					return {"FINISHED"}
		return {"CANCELLED"}


class CreateNNATargetingObjectOperator(bpy.types.Operator):
	"""Creates a new targeting object in the `$nna` root for the specified `target_id`"""
	bl_idname = "nna.create_targeting_object"
	bl_label = "Initializie NNA for this Object"
	bl_options = {"REGISTER", "UNDO"}

	target_id: bpy.props.StringProperty(name = "target_id") # type: ignore
	
	def execute(self, context):
		nna_utils_tree.create_targeting_object(nna_utils_tree.find_nna_root(), self.target_id)
		self.report({"INFO"}, "Targeting object created")
		return {"FINISHED"}


class RemoveNNATargetingObjectOperator(bpy.types.Operator):
	"""Removes the targeting object in the `$nna` root for the specified `target_id`"""
	bl_idname = "nna.remove_targeting_object"
	bl_label = "Remove NNA from this Object"
	bl_options = {"REGISTER", "UNDO"}

	target_id: bpy.props.StringProperty(name = "target_id") # type: ignore

	def invoke(self, context, event):
		return context.window_manager.invoke_confirm(self, event)
	
	def execute(self, context):
		targeting_object = nna_utils_tree.find_nna_targeting_object(self.target_id)
		if(targeting_object):
			nna_utils_json.remove_targeting_object(targeting_object)
			self.report({"INFO"}, "NNA functionality has been removed from: " + self.target_id)
			return {"FINISHED"}
		else:
			self.report({"ERROR"}, "Targeting object not found: " + self.target_id)
			return {"CANCELLED"}


class RemoveNNAJsonComponentOperator(bpy.types.Operator):
	"""Removes a component, specified py `component_index` in the serialized Json definition for the `target_id`"""
	bl_idname = "nna.remove_json_component"
	bl_label = "Remove Json Component"
	bl_options = {"REGISTER", "UNDO"}

	target_id: bpy.props.StringProperty(name = "target_id") # type: ignore
	component_index: bpy.props.IntProperty(name = "component_index", default=-1) # type: ignore

	def invoke(self, context, event):
		return context.window_manager.invoke_confirm(self, event)
	
	def execute(self, context):
		try:
			nna_utils_json.remove_component(self.target_id, self.component_index)
			self.report({'INFO'}, "Component successfully removed")
			return {"FINISHED"}
		except ValueError as error:
			self.report({'ERROR'}, str(error))
			return {"CANCELLED"}


class RemoveNNANameDefinitionOperator(bpy.types.Operator):
	"""Renames a Node (Object or Bone), specified py `target_id` to its original name, without the appended NNA name definition.
	The start index in the name of the NNA definition must be specified in `name_definition_index`.
	"""
	bl_idname = "nna.remove_name_definition"
	bl_label = "Remove Name Definition"
	bl_options = {"REGISTER", "UNDO"}

	target_id: bpy.props.StringProperty(name = "target_id") # type: ignore
	name_definition_index: bpy.props.IntProperty(name = "name_definition_index") # type: ignore

	def invoke(self, context, event):
		return context.window_manager.invoke_confirm(self, event)
	
	def execute(self, context):
		try:
			target = nna_utils_tree.get_object_by_target_id(self.target_id)
			(nna_name, symmetry) = nna_utils_name.get_symmetry(target.name)
			target.name = nna_name[:self.name_definition_index] + symmetry

			self.report({'INFO'}, "Name definition successfully removed")
			return {"FINISHED"}
		except ValueError as error:
			self.report({'ERROR'}, str(error))
			return {"CANCELLED"}
