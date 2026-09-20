/* For license and copyright information please see the LEGAL file in the code repository */

package product_service_p

import (
	product_p "org/modules/economics/product/protocol"
	thing_p "org/modules/identity/thing/protocol"
)

type Model interface {
	thing_p.Model
	product_p.Model
}
