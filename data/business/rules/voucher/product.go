/* For license and copyright information please see the LEGAL file in the code repository */

package voucher

import (
	product_p "org/modules/business/product/protocol"
)

type Product interface {
	Field_Each
	product_p.Field_ProductsID
}
