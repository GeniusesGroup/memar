/* For license and copyright information please see the LEGAL file in the code repository */

package vip

import (
	aap "org/modules/app-audit/protocol"
	fmp "org/modules/financial-money/protocol"
	sp "org/modules/storage/protocol"
	vp "org/modules/voucher/protocol"
)

// TODO::: Currency??

// DataModel indicate the domain record data fields.
type DataModel interface {
	vp.VoucherID
	Each() vp.Each
	MinPrice() fmp.MoneyAmount // Minimum invoice price
	MinAmount() uint64         // Minimum invoice product numbers

	aap.AuditRequest
	sp.SaveTime
}
