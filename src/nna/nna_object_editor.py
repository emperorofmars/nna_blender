import bpy

from .nna_editor import *
from .nna_tree_utils import *
from .nna_operators import *

class NNAEditor(bpy.types.Panel):
	bl_idname = "OBJECT_PT_nna_editor"
	bl_label = "NNA Editor"
	bl_region_type = "WINDOW"
	bl_space_type = "PROPERTIES"
	bl_category = "NNA"
	bl_context = "object"

	@classmethod
	def poll(cls, context):
		return (context.object is not None)

	def draw_header(self, context):
		pass
		
	def draw(self, context):
		match determine_nna_object_state(context.object):
			case NNAObjectState.IsRootObject:
				button = self.layout.operator(CreateNNATargetingObjectOperator.bl_idname, text="Create NNA Component List for Root")
				button.target_id = context.object.name
			case NNAObjectState.IsRootObjectWithTargeting:
				draw_nna_json_editor(self, context, context.object.name)
			case NNAObjectState.NotInited:
				draw_nna_name_editor(self, context, context.object.name)
				self.layout.separator(type="LINE", factor=5)
				if(len(bpy.context.scene.collection.children_recursive) == 0):
					button = self.layout.operator(operator=InitializeNNAOperator.bl_idname, text="Initialize NNA in Scene")
					button.nna_init_collection = bpy.context.scene.collection.name
				else:
					button = self.layout.operator(operator=InitializeNNAOperator.bl_idname, text="Initialize NNA in Collection")
					button.nna_init_collection = context.collection.name
			case NNAObjectState.InitedOutsideTree:
				draw_nna_name_editor(self, context, context.object.name)
				self.layout.separator(type="LINE", factor=5)
				self.layout.label(text="This object is outside the NNA tree!")
			case NNAObjectState.InitedInsideTree:
				draw_nna_name_editor(self, context, context.object.name)
				self.layout.separator(type="LINE", factor=5)
				button = self.layout.operator(CreateNNATargetingObjectOperator.bl_idname, text="Create NNA Component List")
				button.target_id = context.object.name
			case NNAObjectState.IsTargetingObject:
				self.layout.label(text="This is the Json definition for: " + ("The Scene Root" if context.object.name == "$root" else context.object.name[8:]))
			case NNAObjectState.IsJsonDefinition:
				self.layout.label(text="This part of the Json definition for: " + context.object.parent.name[8:])
			case NNAObjectState.HasTargetingObject:
				draw_nna_name_editor(self, context, context.object.name)
				self.layout.separator(type="LINE", factor=5)
				draw_nna_json_editor(self, context, context.object.name)

"""
# TODO Create a new tab in the properties panel
class PropertiesTabTest(bpy.types.Panel):
	bl_idname = "OBJECT_PT_properties_tab_test"
	bl_label = "Properties Tab Test"
	bl_space_type = "PROPERTIES"
	bl_region_type = "NAVIGATION_BAR"

	def draw(self, context):
		self.layout.label(text="Hello World")
"""