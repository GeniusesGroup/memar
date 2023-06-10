/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// BudgetUserRelation indicate the domain record data fields.
type BudgetUserRelation interface {
	BudgetID() BudgetUUID //
	UserID() up.UserUUID
	Type() Relation_Type
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type BudgetUserRelation_StorageServices interface {
	Save(dm BudgetUserRelation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(budgetID BudgetUUID, userID up.UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(budgetID BudgetUUID, userID up.UserUUID, vo protocol.VersionOffset) (dm BudgetUserRelation, nv protocol.NumberOfVersion, err protocol.Error)
}

type Relation_Type uint8

const (
	Relation_Type_Unset Relation_Type = iota
	Relation_Type_Suggester
	Relation_Type_Rectifier
	Relation_Type_Executor
	Relation_Type_Quality_Controller
)
