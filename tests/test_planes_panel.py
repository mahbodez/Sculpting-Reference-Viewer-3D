"""The Planes panel, where the clay is told which armature to build on.

Most of the panel is a straight read and write of settings and is covered by
the modes themselves.  What is worth asserting here is the part that is not:
the bone order shown in the panel is the armature's own bone list, so
reordering it is an edit of the document rather than of the panel, and it has
to undo with everything else and survive a re-derive.  A panel that kept its
own copy of that order would disagree with the form being built from it the
first time a landmark moved.
"""

from __future__ import annotations

import pytest

from refview.core.armature import Armature, ArmatureNode, Bone
from refview.core.settings import PlaneTarget, SculptMode

QtCore = pytest.importorskip("PySide6.QtCore")
QtWidgets = pytest.importorskip("PySide6.QtWidgets")

from refview.ui.panels.planes_panel import PlanesPanel  # noqa: E402 - needs Qt first
from refview.ui.state import ViewerState  # noqa: E402 - needs Qt first


@pytest.fixture(scope="session")
def app():
    """One offscreen Qt application for the run; see test_film_recorder."""
    import os

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    existing = QtWidgets.QApplication.instance()
    yield existing or QtWidgets.QApplication([])


def _wire() -> Armature:
    """A three-boned wire whose bones are named, as a preset's would be."""
    return Armature(
        name="Figure",
        nodes=[
            ArmatureNode(name=f"N{i}", at=(float(i), 0.0, 0.0), size=0.3) for i in range(4)
        ],
        bones=[Bone(0, 1, "Hip L"), Bone(1, 2, "Ribcage"), Bone(2, 3, "Head")],
    )


@pytest.fixture
def panel(app):
    state = ViewerState()
    state.render.planes.enabled = True
    state.render.planes.target = PlaneTarget.GEOMETRY
    state.render.planes.sculpt = SculptMode.ADDITIVE
    state.armatures.add(_wire())
    made = PlanesPanel(state)
    made.refresh()
    return made


def _names(panel) -> list[str]:
    """The bone names in the order list, without the count that prefixes them."""
    return [
        panel._order.item(row).text().split("  ", 1)[1].strip()
        for row in range(panel._order.count())
    ]


def test_the_panel_offers_every_armature_that_has_bones_in_it(panel) -> None:
    panel.state.armatures.add(Armature(name="Empty"))
    panel.refresh_armatures()

    labels = [panel._armature.itemText(row) for row in range(panel._armature.count())]
    assert labels[0].startswith("None")
    assert any("Figure" in label for label in labels)
    assert not any("Empty" in label for label in labels)


def test_picking_an_armature_is_what_the_clay_is_then_built_on(panel) -> None:
    assert panel.state.render.planes.sculpt_armature == -1
    panel._armature.setCurrentIndex(panel._armature.findData(0))
    assert panel.state.render.planes.sculpt_armature == 0
    assert _names(panel) == ["Hip L", "Ribcage", "Head"]


def test_the_order_shown_is_the_armature_s_own_bone_list(panel) -> None:
    panel.state.render.planes.sculpt_armature = 0
    panel.refresh_armatures()
    assert _names(panel) == ["Hip L", "Ribcage", "Head"]

    armature = panel.state.armatures[0]
    armature.bones = armature.with_bone_moved(2, -2)
    panel.refresh_armatures()
    assert _names(panel) == ["Head", "Hip L", "Ribcage"]


def test_moving_a_row_edits_the_armature_and_undoes_with_everything_else(panel) -> None:
    panel.state.render.planes.sculpt_armature = 0
    panel.refresh_armatures()
    panel._order.setCurrentRow(2)
    panel._move_bone(-1)

    armature = panel.state.armatures[0]
    assert [bone.name for bone in armature.bones] == ["Hip L", "Head", "Ribcage"]
    # The row follows the bone it moved, so a second press moves the same one.
    assert panel._order.currentRow() == 1

    assert panel.state.undo()
    assert [bone.name for bone in armature.bones] == ["Hip L", "Ribcage", "Head"]


def test_reordering_leaves_the_wire_itself_alone(panel) -> None:
    """It is a reordering of the making, not a structural edit, so an armature
    derived from a preset is still derived from it afterwards."""
    armature = panel.state.armatures[0]
    armature.preset, armature.derived = "humanoid", True
    was = [node.at for node in armature.nodes]

    panel.state.render.planes.sculpt_armature = 0
    panel.refresh_armatures()
    panel._order.setCurrentRow(0)
    panel._move_bone(1)

    assert armature.derived
    assert [node.at for node in armature.nodes] == was


def test_a_row_past_what_detail_has_bought_is_shown_rather_than_hidden(panel) -> None:
    """The question in front of this list is what one more step of Detail
    would buy, and a row that is not there cannot answer it."""
    planes = panel.state.render.planes
    planes.sculpt_armature = 0
    planes.sculpt_masses = 1
    planes.sculpt_detail = 0.0
    panel.refresh()

    assert panel._order.count() == 3  # every bone is listed
    assert "Detail" in panel._order.item(2).toolTip()
    assert not panel._order.item(0).toolTip()


def test_stone_is_never_offered_an_armature(panel) -> None:
    planes = panel.state.render.planes
    planes.sculpt_armature = 0
    panel.refresh()
    assert panel._sculpt_form.isRowVisible(panel._armature)
    assert panel._sculpt_form.isRowVisible(panel._order_row)

    planes.sculpt = SculptMode.SUBTRACTIVE
    panel.refresh()
    assert not panel._sculpt_form.isRowVisible(panel._armature)
    assert not panel._sculpt_form.isRowVisible(panel._order_row)


def test_an_armature_that_is_gone_reads_as_none(panel) -> None:
    """A session saved with two wires and reopened with one has to come back
    as something, and coming back as no armature is what the mode did before
    there were any."""
    panel.state.render.planes.sculpt_armature = 4
    panel.refresh()

    assert panel._chosen_armature() is None
    assert panel._armature.currentIndex() == 0
    assert panel._order.count() == 0


def test_unticking_a_row_takes_the_clay_off_that_length_of_wire(panel) -> None:
    panel.state.render.planes.sculpt_armature = 0
    panel.refresh_armatures()
    panel._order.item(1).setCheckState(QtCore.Qt.CheckState.Unchecked)

    armature = panel.state.armatures[0]
    assert not armature.bones[1].laid
    assert [bone.name for bone in armature.laid_bones()] == ["Hip L", "Head"]

    assert panel.state.undo()
    assert armature.bones[1].laid


def test_a_bone_taking_no_clay_is_still_listed_so_it_can_be_put_back(panel) -> None:
    armature = panel.state.armatures[0]
    armature.bones[1].laid = False
    panel.state.render.planes.sculpt_armature = 0
    panel.refresh_armatures()

    assert panel._order.count() == 3
    assert panel._order.item(1).checkState() is QtCore.Qt.CheckState.Unchecked
    # Only what is laid is numbered, so the numbering shows the budget moving
    # down to the bones after it.
    assert _names(panel) == ["Hip L", "Ribcage", "Head"]
    assert panel._order.item(0).text().startswith("1.")
    assert panel._order.item(1).text().startswith("--")
    assert panel._order.item(2).text().startswith("2.")


def test_an_armature_with_every_bone_off_stays_pickable(panel) -> None:
    """Or there would be no way to turn one back on."""
    for bone in panel.state.armatures[0].bones:
        bone.laid = False
    panel.refresh_armatures()

    labels = [panel._armature.itemText(row) for row in range(panel._armature.count())]
    assert any("Figure" in label for label in labels)
    assert any("0 of 3 bones" in label for label in labels)


def test_ticking_one_row_of_a_selection_ticks_the_whole_selection(panel) -> None:
    """A limb is four bones, and deciding not to block the arms in is one
    decision.  The selection at the moment of the click is what counts, because
    Qt collapses it on the way to toggling the box."""
    panel.state.render.planes.sculpt_armature = 0
    panel.refresh_armatures()
    for row in (0, 1):
        panel._order.item(row).setSelected(True)
    panel._selected_at_press = panel._selected_rows()
    # Qt would have collapsed the selection by now; the snapshot is the point.
    panel._order.setCurrentRow(0)
    panel._order.item(0).setCheckState(QtCore.Qt.CheckState.Unchecked)

    armature = panel.state.armatures[0]
    assert [bone.laid for bone in armature.bones] == [False, False, True]
    # One decision, so one undo.
    assert panel.state.undo()
    assert [bone.laid for bone in panel.state.armatures[0].bones] == [True, True, True]


def test_ticking_a_row_outside_the_selection_is_that_row_alone(panel) -> None:
    panel.state.render.planes.sculpt_armature = 0
    panel.refresh_armatures()
    for row in (0, 1):
        panel._order.item(row).setSelected(True)
    panel._selected_at_press = panel._selected_rows()
    panel._order.item(2).setCheckState(QtCore.Qt.CheckState.Unchecked)

    assert [bone.laid for bone in panel.state.armatures[0].bones] == [True, True, False]


def test_all_and_none_do_the_whole_list_in_one_step(panel) -> None:
    panel.state.render.planes.sculpt_armature = 0
    panel.refresh_armatures()

    panel._lay_every_bone(False)
    assert not any(bone.laid for bone in panel.state.armatures[0].bones)
    assert panel.state.armatures[0].laid_bones() == []

    panel._lay_every_bone(True)
    assert all(bone.laid for bone in panel.state.armatures[0].bones)

    assert panel.state.undo()
    assert not any(bone.laid for bone in panel.state.armatures[0].bones)


def test_saying_what_is_already_so_is_not_an_undo_step(panel) -> None:
    panel.state.render.planes.sculpt_armature = 0
    panel.refresh_armatures()
    panel._lay_every_bone(True)  # every bone already takes clay
    assert not panel.state.undo()


def test_a_selection_survives_the_list_being_rebuilt(panel) -> None:
    """It is rebuilt on every change, and ticking one row of a selected limb
    would be useless if it dropped the rest of the limb."""
    panel.state.render.planes.sculpt_armature = 0
    panel.refresh_armatures()
    for row in (0, 2):
        panel._order.item(row).setSelected(True)

    panel.refresh_armatures()
    assert panel._selected_rows() == {0, 2}


def test_the_list_and_the_summary_follow_an_edit_without_being_told_to(panel) -> None:
    """The main window connects the document's armature signal to this panel,
    but an edit made from the panel must not need that connection in order to
    show its own result -- a list still showing what it showed before the
    click is a list whose next click means something else."""
    panel.state.render.planes.sculpt_armature = 0
    panel.refresh_armatures()
    assert "3 lengths of wire" in panel._sculpt_count.text()

    panel._lay_every_bone(False)
    assert panel._order.item(0).checkState() is QtCore.Qt.CheckState.Unchecked
    assert panel._order.item(0).text().startswith("--")
    assert "lengths of wire" not in panel._sculpt_count.text()
    assert "0 of 3 bones" in panel._armature.itemText(panel._armature.currentIndex())
