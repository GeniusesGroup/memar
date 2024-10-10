/* For license and copyright information please see the LEGAL file in the code repository */

package voucher

import (
	ebl_p "org/modules/rights/building-location/protocol"
	eb_p "org/modules/rights/building/protocol"
	ep "org/modules/rights/estate/protocol"
)

// Voucher estate is proper or appropriate location indicate specific area not specific location
// It's rule depend on products in invoices e.g. source or destination of taxi as a service(product).
type Estate interface {
	ep.Field_EstateID
	eb_p.Field_BuildingID
	ebl_p.Field_BuildingLocationID
}
