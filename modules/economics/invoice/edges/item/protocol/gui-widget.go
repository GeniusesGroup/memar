/* For license and copyright information please see the LEGAL file in the code repository */

package item_p

import (
	product_p "org/modules/business/product/protocol"
)

type GUI_Widget_Conditions interface {
	product_p.Field_ProductID //
}

type GUI_Widget_Service interface {
	IncrementProductNumber()
	DecrementProductNumber()
}
