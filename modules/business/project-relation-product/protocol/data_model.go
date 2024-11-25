/* For license and copyright information please see the LEGAL file in the code repository */

package prpp

import (
	request_p "memar/audit/request/protocol"
	product_p "org/modules/business/product/protocol"
	project_p "org/modules/business/project/protocol"

	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	project_p.Field_ProjectID
	product_p.Field_ProductID
	Status() Status
	// TODO::: type or label??

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}
