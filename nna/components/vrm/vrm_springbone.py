import bpy

from ...ops.nna_operators_common import EditNNAComponentStringOperator
from ...nna_registry import NNAFunctionType
from ...utils import nna_id_list


_nna_name = "vrm.springbone"


def display_vrm_spring_component(target_id: str, layout: bpy.types.UILayout, json_component: dict, component_index: int):
	nna_id_list.draw_id_list(target_id, layout, json_component, component_index, "colliders")

	row = layout.split(factor=0.4)
	row.label(text="Target None Name")
	row.label(text=json_component.get("target_node_name", "-"))
	edit_target_node_name_button = row.operator(EditNNAComponentStringOperator.bl_idname)
	edit_target_node_name_button.target_id = target_id
	edit_target_node_name_button.component_index = component_index
	edit_target_node_name_button.property_name = "target_node_name"

	row = layout.split(factor=0.4); row.label(text="Raw Springbone Values"); row.label(text=str(json_component.get("parsed")))


nna_types = {
	_nna_name: {
		NNAFunctionType.JsonDisplay: display_vrm_spring_component,
	},
}
