/* For license and copyright information please see the LEGAL file in the code repository */

package inventory_p

import (
	pp "org/modules/product/protocol"
)

type GUI_Widget_Conditions interface {
	ProductUUID() pp.ProductUUID
}

type GUI_Widget_Service interface {
}
