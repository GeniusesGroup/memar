/* For license and copyright information please see the LEGAL file in the code repository */

package upp

type GUI_Page_UsedDomains interface {
	// Staff
	// Content
	// User
	// Group
	// List
	// Timeline
	// Quiddity

	// TODO:::
	// AccessibilityStatus
	// OnlineStatus
}

type GUI_Page_HyperLinks interface {
}

type GUI_Page_Conditions interface {
}

type GUI_Page_Service interface {
	ChangeViewLayout()
	// Block()
	Report()
	SetNotifyType(nt Notify_Type)

	RSSFeed()
}

type Notify_Type uint8

const (
	Notify_Type_Unset Notify_Type = iota
	Notify_Type_Casual
	Notify_Type_All
	Notify_Type_Mute
)
