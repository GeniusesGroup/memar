/* For license and copyright information please see the LEGAL file in the code repository */

package rsp

import (
	aa_p "org/modules/app-audit/protocol"
	fcp "org/modules/financial-currency/protocol"
	fmp "org/modules/financial-money/protocol"
	role_p "org/modules/role/protocol"
	storage_p "org/modules/storage/protocol"
)

// DataModel is fixed negotiated salary that don't follow org||department||role salary rules.
type DataModel interface {
	role_p.Field_RoleID
	fcp.Field_FinancialCurrencyID
	HourlySalary() fmp.MoneyAmount

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}
