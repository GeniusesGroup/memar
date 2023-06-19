/* For license and copyright information please see the LEGAL file in the code repository */

package crp

import (
	vp "org/modules/voucher/protocol"
)

type GUI_Page_UsedDomains interface {
	// Comment
	// User
}

// /invoice?new&pid=[ppppppppppppp]&vid=vvvvvvvvvvv
type GUI_Page_Conditions interface {
	New() bool
	ProductID()
	VoucherID()
}

type GUI_Page_Service interface {
	RegisterVoucher(vid vp.VoucherUUID)
}
