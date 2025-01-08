/* For license and copyright information please see the LEGAL file in the code repository */

package task_p

type Field_Type interface {
	Type() Type
}

type Type uint64

const Type_Unset Type = 0
const (
	Type_TimeBased Type = (1 << iota)

	// It is task template and MUST made other related task when need to do the task in that period.
	// Related task MUST made by rule domain by `rules-engine` not human process.
	// e.g. `Monthly financial report` made this `Financial report - 2024/09`
	// this task types MUST indicate internal process to executes by some related rule
	// e.g. `CFO` or `C level role` MUST approve `Monthly financial report` related tasks.
	Type_Repetitive

	// It is part of a process(project, rule) and MUST NOT do individually.
	Type_ProcessBased
)
