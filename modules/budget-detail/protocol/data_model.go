/* For license and copyright information please see the LEGAL file in the code repository */

package bdp

type DepartmentBudgetDetail_Type uint8

const (
	DepartmentBudgetDetail_Type_Unset DepartmentBudgetDetail_Type = iota
	DepartmentBudgetDetail_Type_Materials
	DepartmentBudgetDetail_Type_Labor
	DepartmentBudgetDetail_Type_Investments
)
