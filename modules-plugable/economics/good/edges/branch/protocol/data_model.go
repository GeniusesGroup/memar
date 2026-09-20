/* For license and copyright information please see the LEGAL file in the code repository */

/*
- product can limit to sell one some physical branch or online store.
*/
package org

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"
	product_p "org/modules/economics/product/protocol"
)

type DataModel interface {
	product_p.Field_ProductID
	BranchID()
	ProviderWarehouse() // TODO::: each product or branch??
	MinStock()
	MaxStock()

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
