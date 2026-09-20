/* For license and copyright information please see the LEGAL file in the code repository */

package pcs_p

// GUICategories indicate the domain record data fields.
type GUICategories interface {
	Content() // HTML
	Style()   // CSS
	Logic()   // JS
}
