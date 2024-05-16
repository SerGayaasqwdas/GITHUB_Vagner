from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from FsmMachine import PasswordState, EmailState, PhoneState
from keyboards import kb_inline_found_values
from data import TEXT_BOT
import re
import logging

loger = logging.getLogger(__name__)
router_regex = Router()
regex_email = re.compile(r'(?:[A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(?:\.[A-Z|a-z]{2,})+')
regex_phone_number = re.compile(r'(?:\+7|8)(?:(?:\d{10})|(?:\(\d{3}\)\d{7})|(?: \d{3} \d{3} \d{2} \d{2})|'
                                r'(?: \(\d{3}\) \d{3} \d{2} \d{2})|(?:-\d{3}-\d{3}-\d{2}-\d{2}))')
str_regex_verify_password = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()]).{8,}$'


async def search_values(message: types.Message, pattern: re.Pattern):
    match_values = re.findall(pattern, message.text)
    loger.debug(f"str = {message.text}, pattern = {pattern}, result = {match_values}")
    if match_values:
        await message.answer(TEXT_BOT.RegexMessage['match_values'].format('\n'.join(match_values)),
                             reply_markup=kb_inline_found_values)
        return match_values
    else:
        await message.answer(TEXT_BOT.RegexMessage["not_match_values"])


@router_regex.message(Command('find_email'), StateFilter(default_state))
async def command_search_email(message: types.Message, state: FSMContext):
    await message.answer(TEXT_BOT.RegexMessage['command_email'])
    await state.set_state(EmailState.InputEmail)


@router_regex.message(Command('find_phone_number'), StateFilter(default_state))
async def command_search_phone_number(message: types.Message, state: FSMContext):
    await message.answer(TEXT_BOT.RegexMessage['command_phone'])
    await state.set_state(PhoneState.InputPhone)


@router_regex.message(Command('verify_password'), StateFilter(default_state))
async def command_verify_password(message: types.Message, state: FSMContext):
    await message.answer(TEXT_BOT.RegexMessage['command_password'])
    await state.set_state(PasswordState.InputPassword)


@router_regex.message(F.text, EmailState.InputEmail)
async def search_email(message: types.Message, state: FSMContext):
    match_values = await search_values(message, regex_email)
    if match_values:
        await state.update_data(emails=match_values)
        await state.set_state(EmailState.EmailFound)
    else:
        await state.clear()


@router_regex.message(F.text, PhoneState.InputPhone)
async def search_phone_number(message: types.Message, state: FSMContext):
    match_values = await search_values(message, regex_phone_number)
    if match_values:
        await state.update_data(phones=match_values)
        await state.set_state(PhoneState.PhoneFound)
    else:
        await state.clear()


@router_regex.message(F.text.regexp(str_regex_verify_password), PasswordState.InputPassword)
async def password_valid(message: types.Message, state: FSMContext):
    await message.answer(TEXT_BOT.RegexMessage['password_difficult'])
    await state.clear()


@router_regex.message(F.text, PasswordState.InputPassword)
async def password_not_valid(message: types.Message, state: FSMContext):
    await message.answer(TEXT_BOT.RegexMessage['password_easy'])
    await state.clear()
