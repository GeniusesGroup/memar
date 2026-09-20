/* For license and copyright information please see the LEGAL file in the code repository */

package role

import (
	"libgo/protocol"
	"libgo/time/utc"
)

type role struct {
	roleID       [16]byte
	parentID     [16]byte
	departmentID [16]byte
	time         utc.Time
	requestID    [16]byte
}

func (r *role) RoleID() [16]byte           { return r.roleID }
func (r *role) ParentID() [16]byte         { return r.parentID }
func (r *role) DepartmentID() [16]byte     { return r.departmentID }
func (r *role) Time() protocol.Time        { return &r.time }
func (r *role) RequestID() UserRequestUUID { return r.requestID }
