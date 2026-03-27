/* For license and copyright information please see the LEGAL file in the code repository */

package op

type GUI_Widget_Conditions interface {
	ObjectID() ObjectUUID
	// show folders and files
}

type GUI_Widget_Services interface {
	// Open a dialog to choose attach files
	Upload()
	Select()

	GetSelectUUID() ObjectUUID
}
