from sqlalchemy import text


UTC_NOW = text("TIMEZONE('utc', NOW())")
