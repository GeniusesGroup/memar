/* For license and copyright information please see the LEGAL file in the code repository */

package best_before_p

import (
	"memar/time/duration"

	product_p "org/modules/economics/product/protocol"
)

type Service_Set_Request interface {
	product_p.Field_ProductID
	Duration() duration.Second // from production time
}
