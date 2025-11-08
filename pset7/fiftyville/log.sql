SELECT name FROM people
-- Query security logs
WHERE people.license_plate IN (
    -- Get the license plates from the courthouse logs
    SELECT license_plate FROM bakery_security_logs
    -- In the ten minute time frame (10:15 - 10:25)
    WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 25
)

-- Query ATM transactions
AND people.id IN (
    -- Get person_id from the ATM transactions
    SELECT person_id FROM bank_accounts
    -- Let's join the bank account information so that we can grab the person_id
    JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
    -- Transaction was on the day of the crime
    WHERE atm_transactions.year = 2020 AND atm_transactions.month = 7 AND atm_transactions.day = 28
    -- It was a withdrawal
    AND transaction_type = "withdraw"
    -- It occured on Fifer Street
    AND atm_transactions.atm_location = "Fifer Street"
)

-- Query calls
AND people.phone_number IN (
    -- Get the phone numbers from calls
    SELECT caller FROM phone_calls
    -- Date of the crime
    WHERE year = 2020 AND month = 7 AND day = 28
    -- Duration less than a minute
    AND duration < 60
)

-- Query first flight passenger list
AND people.passport_number IN (
    -- Get the passport numbers of passengers
    SELECT passport_number FROM passengers
    -- On the first flight
    WHERE flight_id IN (
        -- Get the id of the first flight of the next day
        SELECT id FROM flights WHERE year = 2020 AND month = 7 AND day = 29
        ORDER BY hour, minute ASC LIMIT 1
    )
);
