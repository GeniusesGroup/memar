/* For license and copyright information please see the LEGAL file in the code repository */

package prtp

import (
	"libgo/protocol"

	ltp "org/modules/label-table/protocol"
	pp "org/modules/project/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// Table or boards is visual aid to help users access tasks in GUI e.g.Table(TODO, DOING, DONE)
type DataModel interface {
	ProjectID() pp.ProjectUUID      //
	TableID() ltp.TableUUID         //
	Status() Status                 //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Status qsp.Quiddity_Status
