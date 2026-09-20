/* For license and copyright information please see the LEGAL file in the code repository */

package voucher

import (
	ep "org/modules/identity/estate/protocol"
)

// Voucher estate is proper or appropriate location indicate specific area not specific location
// It's rule depend on products in invoices e.g. source or destination of taxi as a service(product).
type Estate interface {
	ep.Field_EstateID
}
