# Homework 4 solutions

This file is for course administration. Keep it out of the public repository.

## Question 1

**Answer:** `{"status":"ok"}` (option 1).

The `/healthz` endpoint reports that the app and database are available. It does not check every order lookup.

## Question 2

**Answer:** `200` (option 1).

The seeded `standard-1001` order exists, so its lookup succeeds. The request metric should record HTTP status `200` for that request.

## Question 3

**Answer:** `404` (option 1).

There is no seeded order with ID `standard-1002`. Its lookup should appear as a `404` in Grafana, with a corresponding log and trace after the telemetry pipeline is connected.

## Question 4

**Answer:** Normal (option 1).

The request from Question 3 returns `404`. The alert selects `5xx` responses, so it should stay Normal. A well configured rule treats the absence of `5xx` responses as zero errors rather than No data.

## Question 5

**Type:** Free form long; no single exact answer.

The submitted response should quote the last line of the coding agent's answer to the marked `ResponderTest` notification. The wording depends on the student's agent and implementation. A sound response recognises that this is a test notification, reports no confirmed customer incident, and does not deploy a code change.

## Question 6

**Answer:** The express delivery date calculation tried to use a day that does not exist in that month (option 1).

The seeded `express-1002` order is dated on the last day of the previous month. The starter calculates its estimated delivery with `placed_at.replace(day=placed_at.day + 2)`, which can raise `ValueError` because that day number is invalid. Adding two days with `timedelta(days=2)` avoids the month boundary error. After an automated fix, the same lookup should succeed and the `5xx` alert should clear.
