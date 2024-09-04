/* For license and copyright information please see the LEGAL file in the code repository */

package inventory_p

import (
	cl "memar/computer/language"

	aa_p "org/modules/app-audit/protocol"
	np "org/modules/notification/protocol"
	org_p "org/modules/org/protocol"
	product_p "org/modules/product/protocol"
	storage_p "org/modules/storage/protocol"
	wp "org/modules/warehouse/protocol"
)

// ProductInventoryNotify indicate the domain record data fields.
type ProductInventoryNotify interface {
	NotificationID() np.NotificationUUID // user only == timeline-user_notification / staff == any notification group
	product_p.Field_ProductID
	OrgID() []org_p.OrgUUID
	WarehouseID() []wp.WarehouseUUID // user max 2, staff max 10
	AmountOperator() []cl.ComparisonOperator
	Amount() []int64
	StockOperator() []cl.ComparisonOperator
	Stock() []int64

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}

/*
func UserLogic(warehouseID wp.WarehouseUUID, amount int64, stock int64) (notify bool) {
	const desireOrgIDs = []OrgUUID{}
	const warehouseIDs = []wp.WarehouseUUID{}
	if Amount >= 10 {
		return true
	}
	if Amount <= 500 {
		return true
	}
	return
}
*/
