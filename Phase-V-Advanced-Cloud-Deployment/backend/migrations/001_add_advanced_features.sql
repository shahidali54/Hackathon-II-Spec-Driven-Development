-- Migration to add advanced features to the task table
-- Adds columns for priorities, tags, due dates, recurrence rules, and reminders

-- Add priority column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='task' AND column_name='priority') THEN
        ALTER TABLE task ADD COLUMN priority VARCHAR(20) DEFAULT 'medium';
    END IF;
END $$;

-- Add tags column if it doesn't exist (as text array)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='task' AND column_name='tags') THEN
        ALTER TABLE task ADD COLUMN tags TEXT[];
    END IF;
END $$;

-- Add recurrence_rule column if it doesn't exist (as JSON)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='task' AND column_name='recurrence_rule') THEN
        ALTER TABLE task ADD COLUMN recurrence_rule JSONB;
    END IF;
END $$;

-- Add reminder_sent column if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='task' AND column_name='reminder_sent') THEN
        ALTER TABLE task ADD COLUMN reminder_sent BOOLEAN DEFAULT FALSE;
    END IF;
END $$;

-- Create indexes for better performance on new columns
CREATE INDEX IF NOT EXISTS idx_task_priority ON task(priority);
CREATE INDEX IF NOT EXISTS idx_task_tags ON task USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_task_due_date ON task(due_date);
CREATE INDEX IF NOT EXISTS idx_task_reminder_sent ON task(reminder_sent);

-- Create the recurring_task_pattern table
CREATE TABLE IF NOT EXISTS recurring_task_pattern (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES task(id) ON DELETE CASCADE,
    rule JSONB NOT NULL,
    next_occurrence TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Create the reminder table
CREATE TABLE IF NOT EXISTS reminder (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES task(id) ON DELETE CASCADE,
    remind_at TIMESTAMP WITH TIME ZONE NOT NULL,
    sent BOOLEAN NOT NULL DEFAULT FALSE,
    sent_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Create indexes for recurring_task_pattern and reminder tables
CREATE INDEX IF NOT EXISTS idx_recurring_task_pattern_task_id ON recurring_task_pattern(task_id);
CREATE INDEX IF NOT EXISTS idx_recurring_task_pattern_next_occurrence ON recurring_task_pattern(next_occurrence);

CREATE INDEX IF NOT EXISTS idx_reminder_task_id ON reminder(task_id);
CREATE INDEX IF NOT EXISTS idx_reminder_remind_at ON reminder(remind_at);
CREATE INDEX IF NOT EXISTS idx_reminder_sent ON reminder(sent);