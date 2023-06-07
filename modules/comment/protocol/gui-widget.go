/* For license and copyright information please see the LEGAL file in the code repository */

package cp

type GUI_Widget_Settings interface {
	DisableReaction() bool
}

type GUI_Widget_Conditions interface {
	CommentID() CommentUUID //
}

type GUI_Widget_Service interface {
	Save() // TODO::: we need some data model
	Reply()
	Edit()
	Share()
	Delete()
	Pin()
	CopyMessageLink()
	Report()
	ReadBy()

	ChangeSenderUser()
}
