/* For license and copyright information please see the LEGAL file in the code repository */

package iip

type GUI_Widget_Conditions interface {
	ProductID() ProductUUID //
}

type GUI_Widget_Service interface {
	IncrementProductNumber()
	DecrementProductNumber()
}
